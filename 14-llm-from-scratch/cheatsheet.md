# LLM 从零实现速查

## 形状

```text
ids [B,T] → embedding [B,T,d] → attention [B,H,T,T] → logits [B,T,V]
FFN 中间维常见 4d；GQA 的 KV 头数 H_kv < H
```

## 参数量

```text
GPT ≈ V*d + 12*L*d^2
LoRA ≈ r*(d_out+d_in) / 层
```

## 训练算力

```text
FLOPs ≈ 6*N*D
N=参数量，D=训练 token 数
```

## KV cache

```text
bytes = 2*L*H_kv*d_head*T*B*bytes_per_elem
FP16: 2 bytes
```

## 关键公式

$$
\mathcal{L}_{CE}=-\frac{1}{T}\sum_t \log p(x_t|x_{<t})
$$

$$
\text{DPO loss}=-\log\sigma\left(\beta\left[\log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)}-\log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right]\right)
$$

## 最小实验顺序

1. 字符级 tokenizer + 2 层 causal Transformer；
2. 单 batch 过拟合；
3. 小语料预训练；
4. SFT + loss mask；
5. LoRA；
6. 量化/服务；
7. 评测与失败样本。
