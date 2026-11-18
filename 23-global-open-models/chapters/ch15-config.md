# 第 15 章 读 config.json：把架构字段变成可计算的账

> 难度：中高 · 建议 80 分钟 · 前置：第 3、11、13 章
> 学习目标：能独立下载并读取任意开放模型的 `config.json`；能识别 `model_type` 与 `architectures` 的差别；能用字段估算总参数、激活参数和 KV cache；能避开“名字里的参数量”陷阱。

## 一句话核心

模型卡会写营销数字，`config.json` 写结构事实。**先读 config，再信名字。** 你要找的字段只有十几个：层数、hidden、Q/KV 头、head_dim、FFN/专家、top-k、上下文、词表、rope_scaling、dtype。

## 15.1 怎么拿到 config

```python
from huggingface_hub import hf_hub_download
import json

path = hf_hub_download("Qwen/Qwen3.8-27B", "config.json")
cfg = json.load(open(path))
print(cfg.keys())
```

多模态模型的文本参数常藏在 `text_config`：

```python
tc = cfg.get("text_config", cfg)
for k in ["model_type", "num_hidden_layers", "hidden_size",
          "num_attention_heads", "num_key_value_heads",
          "intermediate_size", "max_position_embeddings",
          "vocab_size", "head_dim"]:
    print(k, tc.get(k))
```

> 不要 `trust_remote_code=True` 跑来源不明的仓库；先用 `hf_hub_download` 只下 `config.json`，看字段。需要自定义架构时再读代码。

## 15.2 字段地图

| 字段 | 含义 | 常见坑 |
|---|---|---|
| `architectures` | Python 类名，如 `LlamaForCausalLM` | 同名类可能在不同仓库实现不同 |
| `model_type` | 配置族，如 `llama`、`qwen3_moe` | 多模态顶层 `model_type` 与 `text_config.model_type` 不同 |
| `num_hidden_layers` | 层数 | 多模态塔的层数不在 text_config |
| `hidden_size` | 残差流维度 | 不是 head_dim × heads 一定相等 |
| `num_attention_heads` | Q 头数 | 不是 KV 头数 |
| `num_key_value_heads` | KV 头数 | 缺省时可能等于 Q 头（MHA） |
| `head_dim` | 每头维度 | 很多模型不写，需要从 q_proj 形状推 |
| `intermediate_size` | dense FFN 宽度 | MoE 模型里可能不是专家宽度 |
| `num_experts` / `n_routed_experts` | 路由专家数 | 字段名因家族而异 |
| `num_experts_per_tok` | top-k | 有的模型写在代码里，不在 config |
| `moe_intermediate_size` | 专家 FFN 宽度 | 不等于 dense `intermediate_size` |
| `n_shared_experts` | 共享专家数 | 不是所有 MoE 都有 |
| `max_position_embeddings` | 最大位置 | 可能是外推后的标称值 |
| `rope_scaling` | RoPE 外推配置 | `factor`、`original_max_position_embeddings` 要看 |
| `vocab_size` | 词表大小 | 影响 embedding 和输出头参数 |
| `torch_dtype` / `dtype` | 权重精度 | 实际发布可能是 FP8/BF16 |
| `quantization_config` | 量化方法 | FP8/INT4 会影响显存估算 |

## 15.3 参数量估算

### dense

粗略：

$$
P \approx V H + L\left(4H^2 + 3H F\right)
$$

- $VH$：embedding（若输出头不共享，再加一份）；
- $4H^2$：Q/K/V/O 四个投影（GQA 会少一些）；
- $3HF$：SwiGLU 的三个矩阵。

更精确的注意力项：

$$
P_{attn}=H(H_q d_{head})+2H(H_{kv}d_{head})+H(H_q d_{head})
$$

### MoE

$$
P_{total}\approx VH + L\left(P_{attn}+E\cdot3H F_{exp}+H E\right)
$$

$$
P_{active}\approx VH + L\left(P_{attn}+k\cdot3H F_{exp}+P_{shared}\right)
$$

其中 $E$ 专家数，$k$ top-k，$F_{exp}$ 专家宽度。

> 这些是“数量级估算”，不含 bias、norm、router 细节；算出来和模型卡差 5–10% 很正常。关键是能判断“总参数/激活”量级，不被名字骗。

## 15.4 手算：Qwen3.8-2.4T 的账

字段：$L=92$，$H=8192$，$E=512$，$F_{exp}=2048$，$k=10$。

每个专家：

$$
3\times8192\times2048\approx50.3\text{M}
$$

全部专家：

$$
50.3\text{M}\times512\times92\approx2.37\text{T}
$$

每 token 激活：

$$
50.3\text{M}\times10\times92\approx46.3\text{B}
$$

加上注意力、embedding、共享/路由，接近 95B 激活。**这和 2.4T-A95B 的名字对得上。**

## 15.5 KV 估算

$$
\text{KV/token}=2\times L\times H_{kv}\times d_{head}\times b
$$

Qwen3.8-27B：$L=64$，$H_{kv}=4$，$d_{head}=256$，$b=2$：

$$
2\times64\times4\times256\times2=262{,}144\ \text{bytes}=0.25\ \text{MiB}
$$

128K：$0.25\times131{,}072=32$ GiB。
262K：64 GiB。

> 这是单序列、单模型、FP16 KV。batch 要乘 batch size；KV 量化到 FP8 可减半，INT8 约减半，INT4 约 1/4（有精度代价）。

## 15.6 常见 `model_type` 对照

| `model_type` | 家族 | 备注 |
|---|---|---|
| `llama` | Llama / MiniCPM | 最常见 decoder-only |
| `qwen2` / `qwen3` | Qwen dense | GQA、RoPE |
| `qwen3_moe` | Qwen3 MoE | 128 专家等 |
| `qwen3_next` | Qwen3-Next | 混合线性 |
| `qwen3_5` / `qwen3_5_moe` | Qwen3.5/3.6/3.8 | 多模态常嵌套 text_config |
| `qwen4_exp` | Qwen3.8-Flash-Next | 试验架构 |
| `mistral` / `mixtral` | Mistral / Mixtral | 滑窗/MoE |
| `gemma2` / `gemma3` / `gemma4` | Gemma | 局部/全局、统一多模态 |
| `phi3` | Phi-3/4 | 部分 MHA/GQA |
| `falcon` / `falcon_h1` | Falcon | MQA / 混合 |
| `olmo2` / `olmo3` | OLMo | 开放数据 |
| `glm_moe_dsa` | GLM-5.3 | MoE + DSA |
| `kimi_linear` | Kimi K3 | 线性/混合 |
| `minimax_m3_vl` | MiniMax M3 | 稀疏 MoE + 视觉 |
| `step5` / `step5_vl` | Step-5 | MoE + 感知编码器 |
| `bailing_hybrid` | Ling | 混合 MoE |
| `dots1` | dots.llm1 | MoE |
| `ernie4_5_moe` | ERNIE 4.5 | MoE |

> `model_type` 是配置族，不等于 `architectures` 类名；两者要一起看。

## 15.7 一个最小检查脚本

```python
from huggingface_hub import hf_hub_download
import json

def inspect(model_id):
    cfg = json.load(open(hf_hub_download(model_id, "config.json")))
    tc = cfg.get("text_config", cfg)
    keys = ["model_type", "num_hidden_layers", "hidden_size",
            "num_attention_heads", "num_key_value_heads",
            "intermediate_size", "moe_intermediate_size",
            "num_experts", "n_routed_experts", "num_experts_per_tok",
            "max_position_embeddings", "vocab_size", "head_dim"]
    print(model_id)
    for k in keys:
        if k in tc:
            print(f"  {k}: {tc[k]}")

inspect("Qwen/Qwen3.8-2.4T-A95B")
inspect("google/gemma-4-12B")
```

## 15.8 常见误解

- **“名字里的 2.4T 是激活。”** 看 `A95B` 后缀；A 是 active。
- **“`num_experts` 就是 top-k。”** 不是；top-k 是 `num_experts_per_tok` 或代码里的 `top_k`。
- **“`max_position_embeddings` 就是训练长度。”** 可能是外推后的标称值；看 `rope_scaling.original_max_position_embeddings`。
- **“`hidden_size` 除以 heads 就是 head_dim。”** 很多模型不是（Qwen3.8-27B：5120/24≠256）。
- **“config 里没有就是不存在。”** 多模态塔、视觉/音频参数在别的子 config。

## 15.9 自测

1. `architectures` 和 `model_type` 的区别是什么？
2. 写出 dense 和 MoE 的参数量粗略公式。
3. Qwen3.8-2.4T 的 2.4T 和 95B 分别怎么算出来？
4. 为什么 `max_position_embeddings=262144` 不代表能直接塞 262K？
5. 说出三个容易混淆的字段。

> 参考答案：1）architectures 是类名，model_type 是配置族；2）见 15.3；3）512 专家×3×8192×2048×92≈2.37T；top-10×同式≈46B，加注意力/embedding≈95B；4）训练长度、RoPE 外推、KV 显存限制；5）`num_experts` vs `num_experts_per_tok`、`intermediate_size` vs `moe_intermediate_size`、`max_position_embeddings` vs 实际训练长度。

## 15.10 复习锚点

- 先读 config，再信名字。
- 字段：层数、hidden、Q/KV、head_dim、FFN/专家、top-k、上下文、词表、rope、dtype。
- 公式：dense/MoE 参数、KV。
- `model_type` 对照表。
- 下一章：全球开放权重模型索引，把家族放进一张表。
