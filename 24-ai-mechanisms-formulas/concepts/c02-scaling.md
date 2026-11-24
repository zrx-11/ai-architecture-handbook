# 缩放定律与预算

缩放定律把 loss 画在双对数坐标上，用 \(L(N,D)\approx E+A/N^\alpha+B/D^\beta\) 估“多花算力能买到多少”。它预测 loss，不预测具体能力。

Chinchilla 的修正是“每个参数约配 20 个 token”，但这是给定算力最优；推理量大时，小模型多训数据往往更划算。

必算三项：训练 FLOPs \(6ND\)、训练显存约 16 字节/参数、训练时间 \(6ND/(\text{卡数}\times\text{单卡算力}\times\text{MFU})\)。
