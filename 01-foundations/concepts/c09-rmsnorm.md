# RMSNorm

- **难度**：进阶 | **涉及章节**：第 4 章

## 一句话定义

RMSNorm 用向量的均方根做缩放，不减去均值，比 LayerNorm 少一次统计计算。

## 为什么重要

DeepSeek 全系使用 RMSNorm。它是理解“Pre-Norm 结构为什么能训深”和“训练稳定性”的基础。

## 图示

```mermaid
flowchart LR
  A["输入 x"] --> B["算均方根 rms"]
  B --> C["x / rms"]
  C --> D["乘以可学习缩放 g"]
  D --> E["输出"]
```

## 详解

$$\text{RMSNorm}(x)=\frac{x}{\sqrt{\frac{1}{d}\sum_i x_i^2+\epsilon}}\odot g$$

与 LayerNorm 的差别：LayerNorm 先减均值再除以标准差，RMSNorm 只除以均方根。少了减均值这一步，计算更快，且在 Transformer 上效果差别很小。

$\epsilon$ 是防止除零的小常数，通常取 $10^{-6}$ 量级。$g$ 是每个维度一个可学习参数，让模型自己决定缩放多少。

## 常见误解

- RMSNorm 不是“没有归一化”，它仍然缩放，只是统计量不同。
- 归一化不改变方向，只改变长度，因此不能替代激活函数。

## 在书中出现的脉络

| 章节 | 语境 | 关键结论 |
|---|---|---|
| ch04 | Transformer | 每个子层前做 RMSNorm |
| ch07 | V4 | 保留 RMSNorm，新增 mHC |
| ch09 | V4.1 | 结构与 V4 一致 |

## 相关概念

- 前置：向量
- 后续：Transformer 层、训练稳定性
