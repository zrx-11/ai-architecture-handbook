# 速查表

- 训练 FLOPs：\(6ND\)
- 推理 FLOPs：\(2N\times\text{tokens}\)
- 权重显存：\(N\times b/8\)
- 训练显存：约 16 字节/参数（再加激活）
- KV：\(2L n_{kv}d_h b\,\text{seq}\,\text{batch}\)
- Chinchilla：\(D\approx20N\)
- 总时延：\(\mathrm{TTFT}+\mathrm{TPOT}\times L_{out}\)
- 并发：吞吐 × 平均时延
- LoRA 参数：\(r(d+k)\)
- 量化误差：单权重 \(\le\Delta/2\)，累加约随 \(\sqrt{\text{维度}}\) 放大
