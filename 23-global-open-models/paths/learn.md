# 学习路径：七步走完全球开放模型

这条路径不按公司，按“先会看骨架，再看家族，再看长上下文/多模态，最后会选型”。

## 步骤 1：边界与地图（第 1–2 章）

先分清开放权重/开源/许可证；建立六种骨架的地图。检查点：能用自己的话解释“开放权重不等于开源”。

## 步骤 2：两条主线 Llama 与 Qwen（第 3–4 章）

Llama 看 decoder-only 标准化；Qwen 看密度/MoE/混合的全尺寸树。检查点：能读 70B 和 2.4T-A95B 的 config，算 KV。

## 步骤 3：Mistral、Gemma、Phi（第 5–7 章）

看滑窗、局部/全局、小模型数据路线。检查点：能比较 Mistral 7B、Gemma 3 27B、Phi-4 的 KV。

## 步骤 4：北美与中国其他家族（第 8–9 章）

看 Falcon/BLOOM/OLMo/DBRX/Arctic/Command/Grok，以及 GLM/Kimi/MiniMax/InternLM/MiniCPM/Step/ERNIE/Ling/MiMo。检查点：能列出至少 8 个家族的结构差异与许可证。

## 步骤 5：非 Transformer 与 MoE（第 10–11 章）

看 RWKV/Mamba/Jamba/Griffin/xLSTM/Falcon-H1/Kimi Linear/Qwen3-Next，以及 MoE 的总/激活、路由、共享专家。检查点：能手算 2.4T/95B 的激活比例。

## 步骤 6：多模态与注意力（第 12–13 章）

看图像 token、连接器、早期/晚期融合、Janus，以及 MHA/GQA/MLA/滑窗/稀疏/线性。检查点：能算 448×448 图像 token 和 1M KV。

## 步骤 7：许可证、评测与 config（第 14–16 章）

看许可证矩阵、评测污染、选型矩阵，最后用附录索引查家族。检查点：给定预算和任务，能写出“为什么选它、为什么不选它”。
