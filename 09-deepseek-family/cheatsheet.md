# 速查表

## 配置速查

| 模型 | 总/激活 | 层 | 隐藏 | 头 | 路由/共享 | top-k | 上下文 |
|---|---|---|---|---|---|---|---|
| LLM 7B | 7B | 30 | 4096 | 32/32 | dense | — | 4K |
| LLM 67B | 67B | 95 | 8192 | 64/8 | dense | — | 4K |
| Coder 33B | 33B | 62 | 7168 | 56/8 | dense | — | 16K |
| MoE 16B | 16B/2.8B | 28 | 2048 | 16 | 64+2 | 6 | 4K |
| V2 | 236B/21B | 60 | 5120 | 128 | 160+2 | 6 | 128K |
| V2-Lite | 16B/2.4B | 27 | 2048 | 16 | 64+2 | 6 | 128K |
| Coder-V2 | 236B/21B | 60 | 5120 | 128 | 160+2 | 6 | 128K |
| V3 | 671B/37B | 61 | 7168 | 128 | 256+1 | 8 | 128K |
| R1 | 671B/37B | 61 | 7168 | 128 | 256+1 | 8 | 128K |
| V3.1 | 671B/37B | 61 | 7168 | 128 | 256+1 | 8 | 128K |
| V3.2 | 671B/37B | 61 | 7168 | 128 | 256+1 | 8 | 128K |
| V4-Pro | 1.6T/49B | 61 | 7168 | 128 | 384+1 | 6 | 1M |
| V4-Flash | 284B/13B | 43 | 4096 | 64 | 256+1 | 6 | 1M |
| V4.1-Flash | 552B+196B Engram；8B/16B 激活 | 40（20+20） | — | — | MoE+Engram | — | 1M |
| OCR | 3.3B | 12 | 1280 | 10 | 64+2 | 6 | 8K |
| Prover-V2 | 671B/37B | 61 | 7168 | 128 | 256+1 | 8 | 128K |

## 公式速查

KV cache（MHA，每 token 每层）：

$$
2hd_h\times\text{字节}
$$

MLA（每 token 每层）：

$$
(\text{kv\_lora\_rank}+\text{qk\_rope\_head\_dim})\times\text{字节}
$$

V2 实例：

$$
(512+64)\times2\times60=69{,}120\ \text{B/token}\approx69\ \text{KB}
$$

GRPO 优势：

$$
A_i=\frac{r_i-\operatorname{mean}(r)}{\operatorname{std}(r)}
$$

CED 解码器 KV：

$$
C_l=H_{20}W_l^{KV},\quad l>20
$$

Sinkhorn：

$$
M_{ij}\leftarrow\frac{M_{ij}}{\sum_j M_{ij}},\quad M_{ij}\leftarrow\frac{M_{ij}}{\sum_i M_{ij}}
$$

890 B/token 的 1M 账：

$$
890\ \text{B}\times1{,}000{,}000=890\ \text{MB}
$$

## 许可证速查

| 许可证 | 代表模型 | 要点 |
|---|---|---|
| MIT | V3、R1、V3.1、V3.2、V4、V4.1、Janus | 限制最少，商用友好 |
| Apache 2.0 | Math-V2、OCR2 | 带专利授权，商用友好 |
| DeepSeek Model License | LLM、Coder、MoE、V2、VL/VL2、Prover | 开放权重 + 自定义条款，不是 OSI 开源 |

## 术语速查

- **总参数**：显存。**激活参数**：算力。
- **MLA**：缓存潜向量，不缓存完整 K/V。
- **DSA**：索引器 + top-k。
- **CSA/HCA**：token 维度压缩 + 分层稀疏。
- **CED**：20 层编码 + 20 层解码，解码器复用编码器 KV。
- **Engram**：N-gram 查表，不是矩阵乘。
