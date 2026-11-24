# 推理两阶段

prefill 一次处理整段 prompt，是大矩阵乘、算力密集；decode 逐 token 生成，每次只算一个，带宽密集。

TTFT 主要看 prefill，TPOT 主要看 decode。总时延约 \(\mathrm{TTFT}+\mathrm{TPOT}\times\text{输出长度}\)。

优化方向相反：prefill 看算力、分块与批处理；decode 看 KV 读放大、量化、投机解码与连续批处理。
