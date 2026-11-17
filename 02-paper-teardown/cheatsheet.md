# 速查表

## 关键数字
| 项目 | 数值 |
|---|---|
| R1-Zero AIME 2024 | 15.6% → 71.0% |
| R1 AIME 2024 | 79.8% |
| R1 MATH-500 | 97.3% |
| R1 冷启动数据 | 几千条 |
| R1 SFT 数据 | 约 80 万条（60 万推理 + 20 万通用） |
| R1 蒸馏数据 | 约 8 万条 |
| V4-Pro | 1.6T / 49B，61 层 |
| V4-Flash | 284B / 13B，43 层 |
| CSA 压缩率 | 4:1 |
| HCA 压缩率 | 128:1 |
| V4 1M 上下文 | Pro 27% FLOPs / 10% KV；Flash 10% / 7%（vs V3.2） |
| V4.1-Flash | 552B + 196B Engram，prefill 8B / decode 16B |
| V4.1 全局 KV | 890 B/token |
| V4.1 持久 KV | 约 V4-Flash 的 1/8 |

## 公式
| 场景 | 内容 |
|---|---|
| GRPO 优势 | $A_i=(r_i-\bar r)/\mathrm{std}(r)$ |
| 压缩注意力 | 每 m 个 token 加权压成 1 条 |
| OPD | $\sum_i w_i D_{KL}(\pi_\theta\|\pi_{E_i})$ |
