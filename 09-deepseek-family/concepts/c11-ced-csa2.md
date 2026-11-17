# CED 与 CSA2

- **难度**：高难 | **涉及章节**：第 9 章

## 一句话定义

CED 把模型拆成 20 层编码器 + 20 层解码器，解码器的全局 KV 由编码器末端投影；CSA2 让相邻层复用 KV 和 top-k 索引。

## 为什么重要

V4.1 把 prefill 算力减半、全局 KV 压到 890 B/token，靠的就是这两件结构。

## 详解

CED：编码器 20 层建立全局 KV，解码器 20 层不再自己算，而是：

$$
C_l=H_{20}W_l^{KV},\quad l>20
$$

prefill 只算前 20 层，解码器复用投影。代价是解码器表达受编码器末端限制。

CSA2 三模式：

- Full：重算 KV/index。
- Reindex：复用 KV，重建索引。
- Reuse：复用 KV 和上一层 top-k 索引。

编码器每 6 层一组：1 Full + 5 Reuse；解码器每 4 层一组，首组 Full + 3 Reuse，后四组 Reindex + 3 Reuse。

## 常见误解

- 别以为 CED 是“少训 20 层”——它是编码器-解码器分工。
- 别以为 Reuse 永远正确——分布漂移时要 Reindex。
- 别以为 890 B/token 是全部缓存——只是全局 KV。

## 在书中出现的脉络

| 章节 | 语境 | 关键结论 |
|---|---|---|
| 第 9 章 | V4.1 | 20+20 层，CSA2 复用 |

## 相关概念

- 前置：CSA/HCA、KV cache
- 后续：Engram、DSpark
