# 第 3 章 Llama 家族：decoder-only 的行业基线

> 难度：入门到中级 · 建议 60 分钟 · 前置：第 2 章
> 学习目标：能画出 Llama 1→4 的结构演进；能说清 RoPE、GQA、SwiGLU、RMSNorm 各自解决什么；能区分 Llama 4 的“总参数”和“激活参数”；能手算 Llama 3.3 70B 的 KV cache。

## 一句话核心

Llama 不是“一个模型”，而是一条把 decoder-only Transformer 标准化、再逐步加长上下文和 MoE 的路线。Llama 1 定义了骨架，Llama 2 加了聊天与安全，Llama 3 换了 tokenizer 和规模，Llama 3.1 把上下文拉到 128K，Llama 4 走向 MoE + 多模态 + 超长上下文。

## 3.1 时间线

| 代际 | 发布时间 | 尺寸 | 关键变化 |
|---|---|---|---|
| Llama 1 | 2023-02 | 7B / 13B / 33B / 65B | decoder-only、RoPE、SwiGLU、RMSNorm、2K 上下文 |
| Llama 2 | 2023-07 | 7B / 13B / 70B | 4K 上下文、GQA（70B）、聊天版与安全对齐 |
| Llama 3 | 2024-04 | 8B / 70B | 128K 词表、15T token 训练、8K 上下文 |
| Llama 3.1 | 2024-07 | 8B / 70B / 405B | 128K 上下文、405B 旗舰、工具调用 |
| Llama 3.2 | 2024-09 | 1B / 3B / 11B / 90B | 小尺寸 + 视觉版、轻量端侧 |
| Llama 3.3 | 2024-12 | 70B | 用 70B 接近 405B 的效果，降低部署成本 |
| Llama 4 | 2025-04 | Scout 17B×16E / Maverick 17B×128E | MoE、早期融合多模态、10M/1M 上下文、iRoPE |

> 尺寸写法：`17B×16E` 表示“17B 激活参数 × 16 个专家”；总参数约 109B。Maverick 是 17B×128E，总参数约 400B。**不要把它读成 17B 总参数。**

## 3.2 骨架：Llama 1/2 定下的四个默认值

### RMSNorm

LayerNorm 计算均值方差；RMSNorm 只算均方根：

$$
\text{RMSNorm}(x)=\frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^{d}x_i^2+\epsilon}}\cdot g
$$

它少了一次减均值，数值更稳、计算更省。今天绝大多数开放模型沿用 RMSNorm 或它的变体。

### SwiGLU

FFN 不是简单的 `Linear → 激活 → Linear`，而是：

$$
\text{FFN}(x)=W_2\big(\text{Swish}(W_1x)\otimes W_3x\big)
$$

两个线性投影，一个做门控，一个做值，再逐元素相乘。它在相同参数量下通常比 ReLU FFN 表现更好，代价是 FFN 中间维度要按比例缩小。

### RoPE

位置信息不靠绝对位置 embedding，而是把 Q/K 的向量按位置旋转：

$$
R_{\theta,m} =
\begin{bmatrix}
\cos m\theta & -\sin m\theta\\
\sin m\theta & \cos m\theta
\end{bmatrix}
$$

注意力分数只依赖相对位置 $m-n$。这就是 Llama 能做长度外推的基础；后来加的 YaRN、Llama 3 的 `rope_scaling` 都是在改旋转频率。

### GQA

Llama 2 70B 开始用分组查询注意力：64 个 Q 头共享 8 组 K/V 头。KV cache 直接降到 MHA 的 1/8。

> 注意：Llama 2 的 7B/13B 还是 MHA，Llama 3 的 8B/70B 都是 GQA。不要用“Llama 都用 GQA”这种笼统说法。

## 3.3 代表配置

| 模型 | 层数 | hidden | Q 头 | KV 头 | FFN | 上下文 | 词表 |
|---|---|---|---|---|---|---|---|
| Llama 2 7B | 32 | 4096 | 32 | 32 | 11008 | 4096 | 32000 |
| Llama 3 8B | 32 | 4096 | 32 | 8 | 14336 | 8192 | 128256 |
| Llama 3.1 8B | 32 | 4096 | 32 | 8 | 14336 | 131072 | 128256 |
| Llama 3.1 405B | 126 | 16384 | 128 | 8 | 53248 | 131072 | 128256 |
| Llama 3.3 70B | 80 | 8192 | 64 | 8 | 28672 | 131072 | 128256 |
| Llama 4 Scout | 48 | 5120 | 40 | 8 | 8192（专家内） | 10,485,760 | 202048 |
| Llama 4 Maverick | 48 | 5120 | 40 | 8 | 8192（专家内） | 1,048,576 | 202048 |

> Llama 4 的 `intermediate_size` 是专家内部宽度；总专家数和 top-k 要看 `num_local_experts` / `num_experts_per_tok`。Scout 是 16 专家，Maverick 是 128 专家。

## 3.4 Llama 4 改了什么

### MoE

Scout 和 Maverick 都是 48 层、5120 hidden、40 个 Q 头、8 个 KV 头，但每层 FFN 换成多个专家。Scout 16 专家，Maverick 128 专家；每个 token 只激活一部分，所以激活参数约 17B。

为什么是 17B 激活？因为推理成本主要由激活参数和 KV cache 决定，不是总参数。Scout 总参数 109B，显存要装全部专家；但每 token 计算量接近 17B 模型。Maverick 总参数 400B，激活仍 17B——这就是 MoE 的“容量与算力解耦”。

### iRoPE

Llama 4 不是所有层都用同一个 RoPE。它把注意力层分成“局部/全局”两类，用交错的位置处理支持超长上下文。官方把它叫 iRoPE（interleaved RoPE）。具体实现细节在模型代码里，模型卡没有逐层展开；本册只讲设计意图：**让一部分层专注近处，一部分层保留远距离位置信息**。

### 早期融合多模态

Llama 4 把图像 token 和文本 token 在较早层就拼在一起，而不是只在最后加一个视觉塔。这让模型能做图文推理，但也意味着视觉和语言一起训练，数据配比和算力成本更高。

## 3.5 手算：Llama 3.3 70B 的 KV cache

公式：

$$
\text{KV bytes/token}
=2\times L\times H_{kv}\times d_{head}\times b
$$

其中 $L$ 层数，$H_{kv}$ KV 头数，$d_{head}$ 每头维度，$b$ 每元素字节（FP16=2）。

Llama 3.3 70B：$L=80$，$H_{kv}=8$，$d_{head}=128$，$b=2$。

$$
2\times80\times8\times128\times2=327{,}680\ \text{bytes/token}
\approx 0.3125\ \text{MiB/token}
$$

128K token 的单序列：

$$
327{,}680\times131{,}072
=42{,}949{,}672{,}960\ \text{bytes}
\approx 40\ \text{GiB}
$$

也就是说，**光 KV cache 就约 40 GiB**，还不算权重（70B FP16 约 140 GB）、激活和框架开销。单卡 80GB 想跑 128K，必须量化权重 + KV 量化 + 分页/分离部署，不能拿“模型 70B”直接估。

> 对比 Llama 3.1 8B：32 层、8 KV 头、128 维，每 token 131,072 bytes = 0.125 MiB；128K 约 16 GiB。小模型的长上下文也不是免费。

## 3.6 Llama 的取舍

| 设计 | 得到什么 | 付出什么 |
|---|---|---|
| decoder-only | 训练目标简单、生成灵活 | 没有双向编码，输入理解不如 encoder-decoder |
| RoPE | 相对位置、易外推 | 超长外推需要 YaRN/缩放，频率调不好会退化 |
| GQA | KV cache 降 4–8 倍 | 头数太少会损失表达能力 |
| SwiGLU | 同参数量下效果更好 | FFN 宽度要重新配比 |
| MoE（Llama 4） | 总容量大、激活低 | 显存、路由、专家并行复杂 |
| 社区许可证 | 生态大、工具多 | 商用条款不是 Apache 那种无条件 |

## 3.7 常见误解

- **“Llama 3.1 405B 是 405B 激活。”** 错，它是 dense，405B 总参数也是每 token 激活。
- **“Llama 4 是 17B 模型。”** 错，17B 是激活参数，总参数 109B/400B。
- **“GQA 就是 MQA。”** 错，MQA 是 1 组 KV，GQA 是多组；Llama 2 70B/3 8B 是 8 组。
- **“上下文 128K 就能塞 128K。”** 训练长度、位置外推、KV 显存、注意力精度都会限制实际上限。

## 3.8 自测

1. Llama 1 的四个结构默认值是什么？
2. Llama 2 70B 为什么用 GQA？省的是哪部分显存？
3. Llama 3.3 70B 在 32K 上下文下单序列 KV 约多少 GiB？
4. Llama 4 Scout 和 Maverick 的专家数、总参数、激活参数各是多少？
5. iRoPE 的设计意图是什么？它没有解决什么？

> 参考答案：1）RoPE、SwiGLU、RMSNorm、decoder-only；2）64 个 Q 头共享 8 组 KV，省 KV cache；3）327,680×32,768≈10.7 GB≈10 GiB；4）Scout 16 专家/109B/17B，Maverick 128 专家/400B/17B；5）让局部层和全局层分工支持超长上下文；没有解决 KV 显存和训练数据问题。

## 3.9 复习锚点

- Llama 1→4 的关键变化：RoPE/SwiGLU/RMSNorm → GQA → 128K 词表/128K 上下文 → MoE/多模态/iRoPE。
- 总参数 vs 激活参数：Llama 4 是典型。
- KV 公式：$2 L H_{kv} d_{head} b$。
- 下一章：Qwen 如何把 dense、MoE、多模态、线性注意力全部走一遍。
