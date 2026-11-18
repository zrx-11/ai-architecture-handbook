# 第 9 章 中国开放权重：GLM、Kimi、MiniMax、InternLM 与“多路线并行”

> 难度：中级 · 建议 75 分钟 · 前置：第 8 章
> 学习目标：能列出中国主要开放权重家族；能区分 dense、MoE、线性/稀疏注意力的组合；能读懂 GLM/Kimi/MiniMax/Intern-S2 的 config 字段；能判断许可证不是统一的 Apache。

## 一句话核心

中国开放权重不是“一家一个 Llama 复制品”。GLM 走 MoE + DSA 稀疏注意力，Kimi 走线性注意力 + 超大专家数，MiniMax 走稀疏 MoE + 多模态，InternLM 走 Qwen3.5 MoE 衍生 + 多模态，MiniCPM 走小尺寸端侧，Step/ERNIE/Ling/MiMo 各自有独立的混合/路由设计。

## 9.1 家族速览

| 家族 | 代表 | 结构关键词 | 许可证 | 备注 |
|---|---|---|---|---|
| GLM | GLM-5.3 / 5.3-Flash | MoE + DSA、1M、64/64 MHA | 自定义 | 智谱/Z.ai |
| Kimi | K2 / K2.5 / K3 | 线性注意力 + MoE、896 专家、1M | 自定义 | 月之暗面 |
| MiniMax | M1 / M2 / M3 | 稀疏 MoE、4 KV、1M、视觉 | 自定义 | MiniMax |
| InternLM | InternLM 2.5 / Intern-S2 | Qwen3.5 MoE 衍生、多模态 | Apache 2.0 | 上海 AI Lab |
| MiniCPM | MiniCPM5 / V 4.7 / o 4.5 | 小尺寸 dense、端侧、多模态 | Apache 2.0 | OpenBMB |
| Baichuan | Baichuan 2 / M1 / M2 / Omni | dense、医疗/全模态 | 自定义/Apache | 百川 |
| Yi | Yi 6B/9B/34B / 200K | dense、长上下文 | Apache 2.0 | 零一万物 |
| Step | Step-5-Preview | MoE、1M、视觉感知编码器 | 自定义 | 阶跃星辰 |
| ERNIE | ERNIE 4.5 300B-A47B / 5.5 Flash | MoE、Paddle 生态 | Apache 2.0 | 百度 |
| Ling | Ling 3.0/3.1 | 混合 MoE、512 专家 | MIT | 蚂蚁 inclusionAI |
| MiMo | MiMo-V2.6 | MoE、1M、384 专家 | MIT | 小米 |
| dots | dots.llm1 | MoE、128 专家 + 2 共享 | 自定义 | 小红书 |

> “中国开放权重”不是地理标签，而是发布主体在中国、权重可从 Hugging Face 等公开渠道下载的模型。许可证逐家不同，不能一概说“Apache”。

## 9.2 GLM：MoE + DSA

GLM-5.3 的 config：

- `model_type: glm_moe_dsa`，说明它是 MoE + DSA（稀疏注意力）组合；
- 78 层、6144 hidden、64 Q/64 KV（MHA）、256 路由专家 + 1 共享、top-8、专家宽度 2048、1M 上下文、词表 154880；
- Flash 版 45 层、4096 hidden、288 专家、top-8、1M。

64 个 KV 头 + 1M 上下文，如果按稠密 KV 算会爆炸；DSA 的作用是对注意力做稀疏化/压缩，让长上下文可落地。具体稀疏模式在 `GlmMoeDsaForCausalLM` 实现里，模型卡没有逐行展开；本册只讲设计意图：**不是所有 token 都做全量注意力**。

## 9.3 Kimi：线性注意力 + 896 专家

Kimi K3 的 config：

- 93 层、7168 hidden、96 Q/96 KV、896 专家、1M 上下文、词表 163840；
- 架构标识 `KimiLinearForCausalLM`；
- 带视觉塔，是图文模型。

它是“线性/混合注意力 + 超大 MoE”的组合。96 个 KV 头看起来像 MHA，但如果用了线性注意力，KV 的增长方式不再按 $O(n)$ 存完整 cache；具体层类型要看代码。K2 系列则是 1T 总参数 / 32B 激活级别的 MoE，K3 把专家数推到 896。

**不要用“Kimi 是 Llama 套壳”解释它。** 它的注意力实现和路由规模都和 Llama 不同。

## 9.4 MiniMax：4 个 KV 头的 1M 模型

MiniMax-M3：

- 60 层、6144 hidden、64 Q/4 KV、top-4 + 1 共享专家、1M 上下文、词表 200064；
- 视觉塔 32 层、1280 hidden、16 头；
- 架构 `MiniMaxM3SparseForConditionalGeneration`。

如果按稠密 KV 估算，60 层 × 4 KV × 128 维 × 2 字节 × 2：

$$
2\times60\times4\times128\times2
=245{,}760\ \text{bytes/token}
\approx0.234\ \text{MiB/token}
$$

1M token 约 234 GiB。**1M 上下文不可能靠朴素 KV 硬存**；MiniMax 用稀疏注意力/压缩来降低实际占用。这个数字不是“它真的存了 234 GiB”，而是“如果不做稀疏化，代价会是这样”。

## 9.5 InternLM / Intern-S2：Qwen3.5 MoE 衍生

Intern-S2-397B 的 config：

- 60 层、4096 hidden、32 Q/2 KV、512 专家、top-10、专家宽度 1024、262K、词表 251392；
- `model_type: qwen3_5_moe_text`，架构 `Qwen3_5MoeForConditionalGeneration`；
- 视觉塔 1152 hidden。

它说明一个事实：**开放模型之间会互相复用骨架**。Intern-S2 不是从零写一个新 Transformer，而是在 Qwen3.5 MoE 骨架上做多模态/数据/后训练。读 config 时看到 `qwen3_5_moe`，不要惊讶；这不等于“没有创新”，创新在数据、视觉连接器、训练配方。

## 9.6 MiniCPM：小尺寸端侧

MiniCPM5-2B：

- 42 层、2048 hidden、16 Q/2 KV、FFN 6144、128K、词表 130560；
- `model_type: llama`，`LlamaForCausalLM`；
- Apache 2.0。

它是典型的“小 dense + 长上下文 + 端侧优化”。MiniCPM-V 4.7 35B-A3B 则是多模态 MoE；MiniCPM-o 4.5 是 any-to-any。小尺寸家族也会分叉，不要以为 MiniCPM 只有 2B。

## 9.7 Step / ERNIE / Ling / MiMo / dots

| 模型 | 层数 | hidden | Q/KV | 专家 | top-k | 上下文 | 架构 |
|---|---|---|---|---|---|---|---|
| Step-5-Preview | 92 | 4096 | 64/? | MoE（数量未在 config 展开） | 8 | 1M | `Step5ForCausalLM` + 感知编码器 |
| ERNIE 4.5 300B-A47B | 54 | 8192 | 64/8 | MoE（300B 总/47B 激活） | — | 128K | `Ernie4_5_MoeForCausalLM` |
| Ling 3.1 flash | 72 | 4096 | 64/64 | 512 | 8 | 262K | `BailingMoeV3` 混合 |
| MiMo-V2.6 Pro | 70 | 6144 | 128/8 | 384 | 8 | 1M | `MiMoV2` |
| dots.llm1 | 62 | 4096 | 32/32 | 128 + 2 共享 | 6 | 32K | `Dots1` |

> 表中 `—` 表示模型卡/config 没有给出可靠数字，不硬填。Step-5 的专家总数、ERNIE 的 top-k 在公开 config 里没有直接字段，正文不编造。

## 9.8 许可证：别默认 Apache

| 模型 | 许可证标签 | 商用判断 |
|---|---|---|
| Intern-S2 / MiniCPM5 / ERNIE 4.5 / Yi | Apache 2.0 | 可商用，保留声明 |
| Ling 3.1 / MiMo-V2.6 | MIT | 可商用，保留声明 |
| GLM-5.3 / Kimi K3 / MiniMax M3 / Step-5 / dots | `other` | 逐条读模型卡，可能限制商用/再分发 |
| Baichuan 部分 | 自定义/Apache | 逐模型读 |

> `license: other` 不是“没有许可证”，而是“许可证不在标准 SPDX 列表里”。必须打开模型卡读全文。

## 9.9 自测

1. GLM-5.3 的层数、hidden、Q/KV、专家数、top-k、上下文各是多少？
2. Kimi K3 为什么不能按“Llama 套壳”解释？
3. MiniMax M3 的 4 个 KV 头 + 1M 上下文，朴素 KV 约多少？这说明什么？
4. Intern-S2 的 `model_type` 是什么？这说明了什么？
5. 列出至少三个“中国开放权重但许可证不是 Apache”的模型。

> 参考答案：1）78/6144/64/64/256/top-8/1M；2）`KimiLinearForCausalLM` 线性/混合注意力 + 896 专家，和 Llama 的 MHA/GQA 不同；3）约 234 GiB，说明 1M 必须稀疏/压缩；4）`qwen3_5_moe_text`，说明复用 Qwen3.5 MoE 骨架；5）GLM-5.3、Kimi K3、MiniMax M3、Step-5、dots 等。

## 9.10 复习锚点

- GLM：MoE + DSA，78 层/6144/64/64/256/top-8/1M。
- Kimi：线性 + 896 专家，93 层/7168/96/96/1M。
- MiniMax：60 层/6144/64/4/top-4+1/1M。
- Intern-S2：Qwen3.5 MoE 衍生，60/4096/32/2/512/top-10/262K。
- MiniCPM：2B dense Llama 架构，42/2048/16/2/128K。
- 许可证：Apache/MIT/自定义三分，不统一。
- 下一章：非 Transformer 路线，RWKV、Mamba、Jamba、Falcon-H1、Kimi Linear、Qwen3-Next。
