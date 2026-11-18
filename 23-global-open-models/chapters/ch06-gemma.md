# 第 6 章 Gemma 家族：小模型、局部/全局交替与统一多模态

> 难度：中级 · 建议 60 分钟 · 前置：第 5 章
> 学习目标：能解释 Gemma 2/3 的局部/全局交替为什么省 KV；能说出 Gemma 4 的 any-to-any 架构变化；能比较 Gemma 3 27B 与 Llama 3.3 70B 的 KV 账。

## 一句话核心

Gemma 是 Google 的开放权重线，走的是“小尺寸 + 高质量数据 + 局部/全局交替注意力”的路线。Gemma 2 用 1:1 局部/全局，Gemma 3 用 5:1 局部/全局并加 QK-Norm，Gemma 4 把文本、图像、音频统一进一个 any-to-any 模型。

## 6.1 时间线

| 时间 | 模型 | 关键变化 |
|---|---|---|
| 2024-02 | Gemma 1 2B/7B | 18/28 层，2K/8K 上下文，Gemma Terms |
| 2024-06 | Gemma 2 2B/9B/27B | 局部/全局交替、soft-capping、GQA、8K |
| 2024-10 | RecurrentGemma 2B/9B | Griffin 混合：递归 + 局部注意力 |
| 2024-12 | PaliGemma 2 | SigLIP 视觉 + Gemma 语言模型 |
| 2025-03 | Gemma 3 1B/4B/12B/27B | 128K、5:1 局部/全局、QK-Norm、视觉 |
| 2026-02 | Gemma 4 E2B/E4B | 小尺寸 any-to-any，视觉 + 音频 |
| 2026-06 | Gemma 4 12B | 统一 any-to-any、262K、48 层 |

> Gemma 1–3 的许可证是 Gemma Terms，不是 OSI 认证的开源许可证；Gemma 4 的模型卡标 Apache 2.0。用之前逐个核对，不要一代代类推。

## 6.2 Gemma 2：局部/全局交替

Gemma 2 每两层一组：一层只看局部窗口（4096），一层看全局。局部层省 KV 和计算，全局层保留长距离信息。它还对注意力 logits 做 soft-capping：

$$
\text{logits}' = c\cdot\tanh\left(\frac{\text{logits}}{c}\right)
$$

把过大的 logit 压回范围，训练更稳。这个技巧在 Gemma 2 上有效，但不是所有家族都跟。

| 模型 | 层数 | hidden | Q/KV | FFN | 上下文 | 局部窗口 |
|---|---|---|---|---|---|---|
| Gemma 2 9B | 42 | 3584 | 16/8 | 14336 | 8192 | 4096 |
| Gemma 2 27B | 46 | 4608 | 32/16 | 36864 | 8192 | 4096 |

## 6.3 Gemma 3：5:1 交替 + QK-Norm

Gemma 3 把局部/全局比例改成 5:1：每 6 层里 5 层局部（1024 窗口），1 层全局。这样 128K 上下文下，大部分层只算 1024 窗口，只有少数层承担全局注意力。

QK-Norm 在计算注意力前对 Q 和 K 做归一化：

$$
Q'=\text{RMSNorm}(Q),\qquad K'=\text{RMSNorm}(K)
$$

它能防止 attention logits 随 head_dim 变大而爆炸，是长上下文训练稳定的常用手段。

| 模型 | 层数 | hidden | Q/KV | FFN | 上下文 | 窗口/模式 | 视觉 |
|---|---|---|---|---|---|---|---|
| Gemma 3 4B | 34 | 2560 | 8/4 | 10240 | 131072 | 1024 / 6 | 有 |
| Gemma 3 12B | 48 | 3840 | 16/8 | 15360 | 131072 | 1024 / 6 | 有 |
| Gemma 3 27B | 62 | 5376 | 32/16 | 21504 | 131072 | 1024 / 6 | 有 |

> Gemma 3 27B 的 KV 头是 16，不是 Llama 3.3 70B 的 8；它的 KV cache 反而更大。局部/全局交替省的是“大部分层的窗口”，不是把 KV 头砍到极小。

## 6.4 Gemma 4：any-to-any

Gemma 4 分两条：

- **E2B / E4B**：小尺寸，文本 + 视觉 + 音频。E4B 的文本 42 层、2560 hidden、8 Q/2 KV、131K；视觉塔 16 层/768，音频塔 12 层/1024。
- **12B Unified**：48 层、3840 hidden、16/8、FFN 15360、262K、词表 262144；架构标识 `Gemma4UnifiedForConditionalGeneration`，模型卡标 any-to-any。

“Unified”不是“把三个模型拼在一起”，而是把文本、图像、音频 token 放进同一个自回归序列，用同一套 Transformer 层处理。好处是模态交互深；代价是视觉/音频 token 占用上下文，训练数据配比更难。

| 模型 | 层数 | hidden | Q/KV | FFN | 上下文 | 模态 |
|---|---|---|---|---|---|---|
| Gemma 4 E4B | 42 | 2560 | 8/2 | 10240 | 131072 | 文/图/音 |
| Gemma 4 12B | 48 | 3840 | 16/8 | 15360 | 262144 | 文/图/音 |

## 6.5 手算：Gemma 3 27B 的 KV

$L=62$，$H_{kv}=16$，$d_{head}=128$，FP16：

$$
2\times62\times16\times128\times2
=507{,}904\ \text{bytes/token}
\approx0.484\ \text{MiB/token}
$$

128K：

$$
507{,}904\times131{,}072
=66{,}571{,}926{,}528\ \text{bytes}
\approx62\ \text{GiB}
$$

Gemma 3 4B：$34\times4\times256$ 维，每 token：

$$
2\times34\times4\times256\times2=139{,}264\ \text{bytes}
\approx0.133\ \text{MiB}
$$

128K 约 17 GiB。**小模型的长上下文也要算账，不能看“4B”就以为免费。**

## 6.6 取舍

| 设计 | 得到什么 | 付出什么 |
|---|---|---|
| 局部/全局交替 | 长上下文省计算和 KV | 全局层仍是瓶颈；局部窗口可能丢远处细节 |
| soft-capping | 训练稳定 | 推理时 logit 动态范围被压，可能影响极端置信度 |
| QK-Norm | 大 head_dim 稳定 | 额外归一化开销 |
| 小尺寸 + 强数据 | 端侧可跑 | 容量有限，复杂推理弱于大模型 |
| any-to-any | 模态交互深 | 视觉/音频 token 挤占上下文 |

## 6.7 常见误解

- **“Gemma 3 27B 是 27B 激活。”** 它是 dense，27B 总参数也是每 token 激活。
- **“局部窗口 1024 就是只能看 1024。”** 全局层会跨窗口传递信息；但精确回看远处仍弱于全注意力。
- **“Gemma 4 是 Gemma 3 加一个视觉塔。”** 12B Unified 是统一 any-to-any；E4B 是另一条小尺寸结构。
- **“Gemma 都是 Gemma Terms。”** Gemma 4 的 12B 模型卡标 Apache 2.0；逐模型核对。

## 6.8 自测

1. Gemma 2 的局部/全局比例是多少？Gemma 3 呢？
2. QK-Norm 解决什么问题？
3. Gemma 3 27B 的 KV 头数、head_dim、上下文各是多少？
4. Gemma 4 E4B 的文本/视觉/音频塔规模各是多少？
5. 为什么 Gemma 3 27B 的 KV 比 Llama 3.3 70B 还大？

> 参考答案：1）Gemma 2 约 1:1；Gemma 3 是 5:1（每 6 层 1 层全局）；2）防止大 head_dim 下 attention logits 爆炸，稳定长上下文训练；3）16 KV、128 维、128K；4）文本 42 层/2560，视觉 16 层/768，音频 12 层/1024；5）它 16 个 KV 头，Llama 3.3 70B 只有 8 个，且 head_dim 相同 128。

## 6.9 复习锚点

- Gemma 2：局部/全局 1:1、soft-capping、GQA。
- Gemma 3：5:1、QK-Norm、128K、视觉。
- Gemma 4：E2B/E4B 小尺寸 any-to-any；12B Unified 48 层/3840/16/8/262K。
- 下一章：Phi 的“小模型 + 教科书数据”路线。
