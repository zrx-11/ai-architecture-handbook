# 速查表

## 关键数字
| 项目 | 数值 |
|---|---|
| V3 | 671B / 37B，61 层，MLA，14.8T token |
| V4-Pro | 1.6T / 49B，61 层，CSA+HCA，33T token |
| V4-Flash | 284B / 13B，43 层，CSA+HCA，32T token |
| V4.1-Flash | 552B + 196B Engram，40 层，prefill 8B / decode 16B，45T token |
| V4 1M 效率 | Pro 27% FLOPs / 10% KV；Flash 10% / 7% |
| V4.1 全局 KV | 890 B/token；持久 KV 约 V4-Flash 的 1/8 |
| CSA / HCA | 4:1 / 128:1 |
| R1 后训练 | 冷启动 → RL → 拒绝采样 → RL |
| V4 后训练 | 专家 SFT+GRPO → 10+ 教师 OPD |
| V4.1 后训练 | SFT+RL → 40+ 教师 OPD |

## 公式
| 场景 | 内容 |
|---|---|
| 单请求 KV | token 数 × 每 token 字节 |
| 延迟近似 | max(FLOPs/算力, 字节/带宽) + 调度 |
| OPD | $\sum_i w_i D_{KL}(\pi_\theta\|\pi_{E_i})$ |
