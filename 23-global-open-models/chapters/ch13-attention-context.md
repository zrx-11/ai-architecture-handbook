# 第 13 章 注意力与长上下文：MHA、GQA、MLA、滑窗与线性注意力

> 难度：中高 · 建议 80 分钟 · 前置：第 3、10、11 章
> 学习目标：能区分 MHA/MQA/GQA/MLA 的 KV 结构；能用公式算任意模型的 KV cache；能解释滑窗、局部/全局交替、DSA、线性注意力的取舍；能读 RoPE/YaRN 的 `rope_scaling` 字段。

## 一句话核心

长上下文的第一成本不是“模型能不能记住”，而是 **KV cache 能不能装下**。MHA → MQA → GQA 是在 KV 头上做减法；MLA 是把 KV 压成低秩潜向量；滑窗/局部全局交替是减少每层能看到的 token；DSA/线性注意力是减少每 token 要算的 token。四条路线解决的是同一个账本的不同项。

## 13.1 四种注意力结构

### MHA（多头注意力）

每个 Q 头有独立的 K/V 头。若 $H$ 个 Q 头、$H_{kv}=H$：

$$
\text{KV/token/layer}=2\times H\times d_{head}\times b
$$

表达能力强，KV 最大。

### MQA（多查询注意力）

所有 Q 头共享 1 组 K/V，$H_{kv}=1$。KV 降到 MHA 的 $1/H$。Falcon 7B 是典型。

### GQA（分组查询注意力）

Q 头分成 $G$ 组，每组共享 1 组 K/V，$H_{kv}=G$。Llama 3、Qwen、Gemma、Phi-4 都用。$G$ 常为 2/4/8/16。

### MLA（多头潜在注意力）

不直接存 K/V，而是先把 K/V 压到一个低秩潜向量 $c_t$，推理时再投影出 K/V。DeepSeek V2/V3 用。KV cache 从“每层 $2H d_{head}$”降到“每层 $d_c$ + 少量 RoPE 维度”，压缩比很高。

> MLA 的代价是实现复杂、训练要调投影矩阵；它不是“免费压缩”，而是用低秩假设换显存。

## 13.2 跨家族 KV 对比

| 模型 | 层数 | Q 头 | KV 头 | head_dim | 上下文 | KV/token（FP16） |
|---|---|---|---|---|---|---|
| Llama 3.3 70B | 80 | 64 | 8 | 128 | 128K | 0.3125 MiB |
| Qwen3.8-27B | 64 | 24 | 4 | 256 | 262K | 0.25 MiB |
| Qwen3.8-2.4T-A95B | 92 | 64 | 4 | 256 | 262K | 0.359 MiB |
| Gemma 3 27B | 62 | 32 | 16 | 128 | 128K | 0.484 MiB |
| Phi-4 | 40 | 40 | 10 | 128 | 16K | 0.195 MiB |
| MiniMax M3 | 60 | 64 | 4 | 128 | 1M | 0.234 MiB |
| Mistral Large 4 | 72 | 64 | 64 | 96? | 1M | 1.72 MiB? |
| GLM-5.3 | 78 | 64 | 64 | 192 | 1M | 3.66 MiB |
| Falcon 7B | 32 | 71 | 1（MQA） | 64 | 4K | 0.0078 MiB |

> 表中 `?` 表示 head_dim 没有在 config 直接给出，按 hidden/heads 推可能不准；不要拿它做精确部署估算。Mistral Large 4 的 64 个 KV 头 + 1M 上下文，朴素 KV 会非常大，实际依赖 FP8/稀疏/分页。

## 13.3 手算：1M 上下文到底多大

以 MiniMax M3 为例：

$$
2\times60\times4\times128\times2
=245{,}760\ \text{bytes/token}
$$

1M token：

$$
245{,}760\times1{,}048{,}576
=257{,}698{,}037{,}760\ \text{bytes}
\approx240\ \text{GiB}
$$

Qwen3.8-2.4T：

$$
2\times92\times4\times256\times2=376{,}832\ \text{bytes/token}
$$

1M 约 368 GiB。

Gemma 3 27B 在 1M 下约 496 GiB。

**所以 1M 上下文模型不可能靠朴素 KV 硬存**。它们必须用以下至少一种：

- GQA/MQA 把 KV 头砍到 2–8；
- MLA 把 KV 压成低秩；
- 滑窗/局部全局交替，只让少数层看全局；
- DSA/稀疏注意力，每 token 只选部分历史；
- KV 量化（FP8/INT8）；
- 分页/分离部署（PagedAttention、KV offload）。

## 13.4 滑窗与局部/全局交替

Mistral 7B：窗口 4096，序列超过窗口后旧 token 滚出；KV 只保留窗口。

Gemma 2：1:1 局部/全局；Gemma 3：5:1（每 6 层 1 层全局）。局部层窗口 1024，全局层看全序列。

优点：大部分层 KV 和计算按窗口算，长上下文成本大降。
缺点：全局层仍是瓶颈；局部窗口可能丢远处细节。

## 13.5 DSA / 稀疏注意力

DSA（DeepSeek Sparse Attention）这类方法的核心是：**不是每个 token 都和全部历史做注意力，而是用一个轻量索引器选 top-k 个相关 token**。GLM-5.3 的 `glm_moe_dsa`、DeepSeek V3.2/V4 的 DSA/CSA 都属于这条路线。

代价：

- 索引器本身要训练；
- top-k 选错会丢信息；
- 实现比标准注意力复杂；
- 长上下文效果依赖训练数据。

## 13.6 RoPE / YaRN

RoPE 把 Q/K 按位置旋转。YaRN 通过改旋转频率、温度，把训练长度外推：

```json
"rope_scaling": {
  "rope_type": "yarn",
  "factor": 8.0,
  "original_max_position_embeddings": 8192
}
```

`factor=8` 表示把 8K 训练长度外推到 64K 量级。它不是“免费变长”：外推过头会退化，需要长文本继续训练。

Llama 3.1 的 `rope_scaling` 是 `llama3` 类型，`factor=8`、`original_max_position_embeddings=8192`，所以 8K→128K。Qwen3.5/3.8 直接训到 262K，不再依赖大幅外推。

## 13.7 常见误解

- **“KV 头数等于 Q 头数。”** 只有 MHA 是；GQA/MQA 不是。
- **“head_dim = hidden / heads。”** 很多模型不是整数关系（Qwen3.8 27B：hidden 5120、24 头、head_dim 256）。
- **“上下文长度 = 训练长度。”** 标称最大位置可能靠 YaRN 外推，实际能力要看训练数据。
- **“MLA 只省显存，不影响效果。”** 低秩压缩有信息损失；DeepSeek 用训练和 RoPE 设计来补。
- **“稀疏注意力一定更快。”** 索引器、top-k、不规则内存访问可能吃掉收益；要看实现和 batch。

## 13.8 自测

1. MHA、MQA、GQA 的 KV 头数关系是什么？
2. 用公式算 Llama 3.3 70B 在 32K 下的 KV。
3. 为什么 1M 上下文模型必须做稀疏/压缩？
4. Gemma 3 的局部/全局比例是多少？它省的是哪部分？
5. YaRN 的 `factor` 和 `original_max_position_embeddings` 各表示什么？

> 参考答案：1）MHA：$H_{kv}=H$；MQA：$H_{kv}=1$；GQA：$H_{kv}=G<H$；2）327,680×32,768≈10 GiB；3）朴素 KV 可达数百 GiB，必须 GQA/MLA/稀疏/量化；4）5:1，省局部层的 KV 和计算；5）factor 是外推倍数，original 是原训练长度。

## 13.9 复习锚点

- 四种注意力：MHA、MQA、GQA、MLA。
- KV 公式：$2LH_{kv}d_{head}b$。
- 长上下文五件套：GQA/MLA、滑窗、稀疏、量化、分页。
- RoPE/YaRN：`factor`、`original_max_position_embeddings`。
- 下一章：许可证、数据与评测，避免“下载了却不能商用”。
