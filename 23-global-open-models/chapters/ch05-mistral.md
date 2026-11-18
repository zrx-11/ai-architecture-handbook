# 第 5 章 Mistral 家族：滑窗、MoE 与多模态的三次转向

> 难度：中级 · 建议 60 分钟 · 前置：第 4 章
> 学习目标：能说清 Mistral 7B 的滑窗注意力为什么省 KV；能区分 Mixtral 的“总参数/激活参数”；能列出 Mistral Small/Medium/Large 4 的结构差异。

## 一句话核心

Mistral 的路线不是“越大越好”，而是三次转向：先用**滑窗注意力**把 7B 做到长上下文；再用 **MoE** 把容量和激活拆开；最后用 **Pixtral/Voxtral** 把图像和音频接进来。它是最早把“开放权重 + 商业许可”做成产品线的欧洲家族。

## 5.1 时间线

| 时间 | 模型 | 结构关键词 |
|---|---|---|
| 2023-09 | Mistral 7B | 32 层、4096 hidden、GQA 8 KV、滑窗 4096、32K 上下文 |
| 2023-12 | Mixtral 8x7B | 8 专家、top-2、总 46.7B / 激活 12.9B |
| 2024-01 | Mixtral 8x22B | 8 专家、top-2、总 141B / 激活 39B、64K 上下文 |
| 2024-05 | Codestral 22B | 代码专用、32K 上下文 |
| 2024-09 | Pixtral 12B | 视觉编码器 + 语言模型 |
| 2025-01 | Mistral Small 3 24B | 40 层、5120 hidden、32/8 GQA、128K |
| 2025-03 | Mistral Small 3.1 24B | 多模态 instruct、Apache 2.0 |
| 2025-06 | Magistral / Voxtral | 推理模型、音频模型 |
| 2026-03 | Mistral Small 4 119B | 36 层、4096、32/32、128 专家 top-4、1M |
| 2026 | Mistral Large 4 1T-A52B | 72 层、6144、64/64、128 路由专家 + 1 共享、top-4、1M、FP8 |

> 2026 的 Small 4 / Large 4 配置来自 Hugging Face `config.json`；Large 4 的权重以 FP8 发布，部署门槛比“1T”听起来低，但仍然需要多卡。

## 5.2 Mistral 7B：滑窗注意力

标准注意力每个 token 都要看前面所有 token，KV cache 随序列长度线性增长，注意力计算随长度平方增长。Mistral 7B 把每个 token 的可见范围限制在最近 $W=4096$ 个 token：

$$
\text{Attn}(Q,K,V)=\text{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right)V,
\quad K,V \in \mathbb{R}^{W\times d}
$$

序列超过 4096 时，旧 token 被滚出窗口。这样 KV cache 只保留窗口内的 K/V，显存不随 32K 线性涨。

代价：**模型不能直接回看窗口外的原文**。它靠层叠的窗口把信息逐层传递，但精确检索远处 token 的能力弱于全注意力。后来的 Gemma 2/3 用“局部/全局交替”来补这个缺陷。

## 5.3 Mixtral：MoE 的早期模板

Mixtral 8x7B 不是“8 个 7B 模型拼起来”。它每层有 8 个专家 FFN，每个 token 由路由器选 top-2 专家：

$$
y=\sum_{i\in \text{top-2}(g(x))} g_i(x)\,E_i(x)
$$

总参数约 46.7B（8 个专家 + 注意力 + embedding），每 token 激活约 12.9B（2 个专家 + 共享部分）。8x22B 同理：总 141B，激活 39B。

| 模型 | 层数 | hidden | Q/KV | 专家 | top-k | 总参/激活 | 上下文 |
|---|---|---|---|---|---|---|---|
| Mixtral 8x7B | 32 | 4096 | 32/8 | 8 | 2 | 46.7B / 12.9B | 32K |
| Mixtral 8x22B | 56 | 6144 | 48/8 | 8 | 2 | 141B / 39B | 64K |

> 注意：8x7B 的“7B”是单个专家的宽度量级，不是总参数；总参数还要加注意力和 embedding。

## 5.4 Mistral Small / Medium / Large 4

### Small 3.1 24B

40 层、5120 hidden、32 Q 头、8 KV 头、128K 上下文。它是 24B 级多模态 instruct，视觉塔是 Pixtral 风格。Apache 2.0，适合单卡 48GB 量化部署。

### Small 4 119B

36 层、4096 hidden、32 Q 头、32 KV 头（MHA）、128 路由专家、top-4、专家宽度 2048、1M 上下文。这个配置有两个反直觉点：

1. **只有 36 层**，但 hidden 4096、专家 128 个，总参数 119B；
2. **KV 头 32 个，不是 GQA**，所以 1M 上下文的 KV cache 非常贵。

它的设计更像是“宽而浅的 MoE + 强长上下文”，不是“深而窄的 dense”。

### Medium 3.5 128B

88 层、12288 hidden、96 Q 头、8 KV 头、FFN 28672、262K 上下文。它是 dense，不是 MoE；hidden 12288 比 Large 4 的 6144 宽一倍。宽模型单层表达能力强，但层数少、显存带宽压力大。

### Large 4 1T-A52B

72 层、6144 hidden、64 Q 头、64 KV 头（MHA）、128 路由专家 + 1 共享专家、top-4、专家宽度 6144、1M 上下文。官方以 FP8 权重发布，视觉塔是 Pixtral（30 层、2048 hidden）。

| 模型 | 层数 | hidden | Q/KV | 专家 | top-k | 上下文 | 类型 |
|---|---|---|---|---|---|---|---|
| Small 3.1 24B | 40 | 5120 | 32/8 | dense | — | 128K | dense + 视觉 |
| Small 4 119B | 36 | 4096 | 32/32 | 128 | 4 | 1M | MoE + 视觉 |
| Medium 3.5 128B | 88 | 12288 | 96/8 | dense | — | 262K | dense |
| Large 4 1T-A52B | 72 | 6144 | 64/64 | 128 + 1 共享 | 4 | 1M | MoE + 视觉 |

## 5.5 手算：Mistral 7B 的 KV 账

Mistral 7B：$L=32$，$H_{kv}=8$，$d_{head}=128$，FP16。

$$
2\times32\times8\times128\times2
=131{,}072\ \text{bytes/token}
=0.125\ \text{MiB/token}
$$

32K token：$131{,}072\times32{,}768=4{,}294{,}967{,}296$ bytes ≈ 4 GiB。

如果是 32 个 KV 头的 MHA：

$$
2\times32\times32\times128\times2
=524{,}288\ \text{bytes/token}
=0.5\ \text{MiB/token}
$$

32K 约 16 GiB。**GQA 在这里省了 4 倍。**

## 5.6 取舍

| 设计 | 得到什么 | 付出什么 |
|---|---|---|
| 滑窗 | KV 小、长序列可跑 | 不能精确回看远处 |
| MoE | 总容量大、激活低 | 显存装全部专家、路由通信 |
| 宽 hidden（Medium） | 单层表达强 | 显存带宽和矩阵乘成本高 |
| MHA（Small 4 / Large 4） | 表达能力强、实现简单 | 1M 上下文 KV 巨大 |
| 多模态 | 图文/音频 | 视觉 token 预算、训练数据 |

## 5.7 常见误解

- **“Mistral 7B 支持 32K，所以能直接塞 32K。”** 它用 4096 滑窗，32K 是最大位置；超出窗口的信息靠层间传递，不是精确注意力。
- **“Mixtral 8x7B 是 56B 激活。”** 总参数 46.7B，激活 12.9B。
- **“Small 4 是 GQA。”** 它 32 个 KV 头，是 MHA；不要看“Small”就默认省 KV。
- **“Large 4 是 1T 激活。”** 1T 总参数，52B 激活。

## 5.8 自测

1. Mistral 7B 的滑窗大小是多少？它省的是哪部分显存？
2. Mixtral 8x7B 的总参数和激活参数各是多少？
3. Mistral Small 4 119B 的层数、KV 头数、专家数、上下文各是多少？
4. Mistral Large 4 1T-A52B 的专家结构和激活参数是什么？
5. 滑窗注意力最大的能力缺陷是什么？

> 参考答案：1）4096；省 KV cache（只保留窗口内）；2）46.7B / 12.9B；3）36 层、32 KV、128 专家 top-4、1M；4）128 路由 + 1 共享，top-4，52B 激活；5）不能精确回看窗口外原文。

## 5.9 复习锚点

- Mistral 7B：滑窗 4096 + GQA 8 KV。
- Mixtral：8 专家 top-2，8x7B 46.7B/12.9B，8x22B 141B/39B。
- Small 4 119B：36 层、32/32 MHA、128 专家 top-4、1M。
- Large 4：72 层、64/64、128+1 专家、top-4、1M、FP8。
- 下一章：Gemma 怎么用局部/全局交替和小模型路线。
