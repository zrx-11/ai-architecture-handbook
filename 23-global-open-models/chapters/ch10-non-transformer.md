# 第 10 章 非 Transformer：RWKV、Mamba、Jamba 与混合注意力

> 难度：中高 · 建议 80 分钟 · 前置：第 3 章、第 9 章
> 学习目标：能区分线性注意力、状态空间模型（SSM）和混合架构；能写出 SSM 的递归式；能说清“线性复杂度”换来了什么、失去了什么；能识别 Kimi Linear、Qwen3-Next、Falcon-H1 的混合设计。

## 一句话核心

Transformer 的注意力是“每个 token 和前面所有 token 两两算”，复杂度 $O(n^2)$、KV cache 随长度线性涨。非 Transformer 路线用**递归状态**或**线性核**把复杂度降到 $O(n)$，但把“精确回看任意位置”压缩进一个固定大小的状态。混合架构用少量全注意力层补回精确检索。

## 10.1 三条路线

| 路线 | 代表 | 核心机制 | 复杂度 |
|---|---|---|---|
| 线性注意力 / RNN 化 | RWKV、Kimi Linear、Qwen3-Next | 用递归状态或核函数替代 softmax 注意力 | $O(n)$ |
| 状态空间模型 SSM | Mamba、Mamba-2、Falcon-H1 | 连续状态递推，选择性扫描 | $O(n)$ |
| 混合 | Jamba、Griffin、RecurrentGemma、Falcon-H1、Kimi K3、Qwen3-Next | 线性层 + 少量全注意力层 | 接近 $O(n)$，局部 $O(n^2)$ |

> “非 Transformer”不是“没有 Transformer 层”。Jamba、Falcon-H1、Kimi K3 都保留了一部分注意力；准确说法是“混合架构”。

## 10.2 SSM 的递推式

一个最简状态空间层：

$$
h_t = A h_{t-1} + B x_t
$$

$$
y_t = C h_t
$$

$h_t$ 是固定维度的状态，$x_t$ 是当前 token 的输入。每来一个 token，只做一次矩阵乘和加法，不保存前面所有 token 的 K/V。序列长度 $n$ 的计算量是 $O(n)$，显存是 $O(1)$（相对长度）。

Mamba 的关键是“选择性”：$B$、$C$、$\Delta$ 由输入动态决定，让模型能选择记住/忘记什么。Mamba-2 把选择性 SSM 写成更适合 GPU 的矩阵形式。

**代价**：状态维度固定，长序列的细节会被压缩。需要精确查找某个早期 token 时，SSM 不如全注意力。

## 10.3 RWKV：RNN 化 Transformer

RWKV 把 Transformer 的注意力拆成两个模块：

- **time-mix**：沿时间轴混合历史信息，递归更新；
- **channel-mix**：沿特征维混合，类似 FFN。

它的推理可以像 RNN 一样逐 token 递推，训练又能并行。RWKV-4/5/6/7 逐步改进数值稳定性和状态容量；RWKV-7 引入更灵活的动态状态。

RWKV 的优势是**常数显存、长序列推理**；劣势是状态容量有限，复杂检索/长程依赖不如全注意力。

## 10.4 Mamba / Jamba / Griffin / xLSTM

| 模型 | 机制 | 规模 | 上下文 | 备注 |
|---|---|---|---|---|
| Mamba | 选择性 SSM | 130M–2.7B / 7B 级 | 视版本 | 纯 SSM |
| Mamba-2 | 结构化 SSM + GPU 优化 | 130M–? | 视版本 | 更快 |
| Jamba | Transformer + Mamba 混合，比例约 1:7? | 52B 总/12B 激活 | 256K | AI21 |
| Griffin | RG-LRU + 局部注意力 | 2B/9B（RecurrentGemma） | 视版本 | DeepMind |
| xLSTM | 指数门控 + 矩阵记忆 | 7B 级 | 视版本 | 2024 |
| Falcon-H1 | Mamba/Transformer 混合 | 7B/34B? | 262K | TII |
| Kimi Linear | KDA 线性注意力 + 少量全注意力 | 93 层/7168 | 1M | Kimi K3 |
| Qwen3-Next | Gated DeltaNet + Gated Attention | 80B-A3B | 262K | 阿里 |

> Jamba 的混合比例在不同资料里有 1:7、1:3 等说法；读具体模型卡/论文，不要背一个固定比例。本表只标“混合”。

## 10.5 Kimi Linear 与 Qwen3-Next

### Kimi K3

93 层、7168 hidden、96 Q/96 KV、896 专家、1M 上下文，架构 `KimiLinearForCausalLM`。它不是“每层都全注意力”，而是把线性注意力（KDA，Kimi Delta Attention）和少量全注意力层混合。线性层负责长序列的常数显存，全注意力层负责精确检索。

### Qwen3-Next

48 层、2048 hidden、16 Q/2 KV、512 专家、top-10、262K。它用 Gated DeltaNet（线性注意力） + Gated Attention 的混合；大部分层是线性，少量层是全注意力。它的 80B 总参数 / 3B 激活，是“线性 + MoE”的组合。

> 这两个模型说明 2025–2026 的趋势：**不是纯线性替代 Transformer，而是混合**。纯线性在长序列便宜，但精确回看和 in-context learning 弱；全注意力强，但长序列贵。

## 10.6 手算：注意力 vs 状态

假设序列长度 $n=131{,}072$，hidden $d=4096$，FP16。

### 全注意力

注意力分数矩阵大小 $n\times n$，即使不存完整矩阵，计算也要 $O(n^2 d)$。KV cache 每层约 $2n d$ 字节（MHA 近似），32 层就是：

$$
2\times32\times131{,}072\times4096\times2
\approx 68.7\ \text{GB}
$$

（实际 GQA 会小很多；这里用 MHA 说明量级。）

### SSM

状态 $h$ 的维度是固定的（比如 16–128），每层只存 $O(d h)$，与 $n$ 无关。128K 序列的显存不会按 128K 线性涨。

**但**：状态容量固定，早期细节会丢。混合架构就是“大部分层用 SSM/线性，少数层用全注意力”。

## 10.7 常见误解

- **“线性注意力一定比 Transformer 快。”** 短序列、训练前期、核函数开销可能吃掉收益；长序列、大 batch 才明显。
- **“Mamba 没有注意力，所以不能检索。”** 它有意选择性状态，能记住一部分；只是不能精确回看所有位置。
- **“Jamba 是纯 Mamba。”** 它是 Transformer + Mamba 混合。
- **“Kimi K3 是 96 个 KV 头的 MHA。”** 它用线性/混合注意力，KV 增长方式不同；96 是 Q 头数，不等于每层都存 96 组 KV。
- **“非 Transformer 一定更省显存。”** 权重可能更大，训练并行更复杂；省的是长序列的激活/KV。

## 10.8 自测

1. 写出 SSM 的递推式，并说明 $h_t$ 的维度为什么不随序列长度涨。
2. RWKV 的 time-mix 和 channel-mix 各做什么？
3. Jamba、Griffin、Falcon-H1 各自混合了什么？
4. Kimi K3 和 Qwen3-Next 的混合注意力有什么共同点？
5. 为什么纯线性模型在长上下文检索上可能弱于全注意力？

> 参考答案：1）$h_t=Ah_{t-1}+Bx_t$，$y_t=Ch_t$；$h$ 是固定维度状态；2）time-mix 沿时间递归混合历史，channel-mix 沿特征维做 FFN 式混合；3）Jamba=Transformer+Mamba，Griffin=RG-LRU+局部注意力，Falcon-H1=Mamba/Transformer 混合；4）大部分层线性、少量层全注意力；5）固定状态压缩了历史，不能精确回看任意位置。

## 10.9 复习锚点

- 三条路线：线性注意力、SSM、混合。
- SSM 递推：$h_t=Ah_{t-1}+Bx_t$，$y_t=Ch_t$。
- RWKV：time-mix + channel-mix。
- 混合代表：Jamba、Griffin、Falcon-H1、Kimi K3、Qwen3-Next。
- 下一章：MoE 世界，把“总参数/激活参数”彻底算清。
