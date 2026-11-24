# KV cache

自回归生成时，第 n 个 token 的注意力需要前面所有 token 的 K、V。缓存下来，每步只算新 token，显存随上下文线性增长。

公式：\(2\times L\times n_{kv}\times d_{head}\times\text{bytes}\times\text{seq}\times\text{batch}\)。系数 2 是 K 和 V。

优化路线：GQA 共享 K/V；MLA 压成低秩潜向量；PagedAttention 分页；KV 量化；驱逐时保留开头 Attention Sink。
