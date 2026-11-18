# 第 8 章 北美开放权重：Falcon、BLOOM、OLMo、DBRX 与“非 Llama”路线

> 难度：中级 · 建议 70 分钟 · 前置：第 7 章
> 学习目标：能列出北美主要开放权重家族及其架构差异；能区分“模型开放”“数据开放”“许可证开放”；能用 KV 公式比较 BLOOM、MPT、Falcon 的部署成本。

## 一句话核心

北美开放权重不是“Llama 的复制品”。Falcon 走 MQA + 早期多语言，BLOOM 走超大 dense + 多语言，MPT 走 ALiBi 长上下文，OLMo 走“数据/代码全开放”，DBRX/Arctic 走 MoE，Command R 走非商用许可，Grok-1 走超大 MoE。它们共同构成“Llama 之外的对照组”。

## 8.1 家族速览

| 家族 | 代表 | 结构关键词 | 许可证 | 备注 |
|---|---|---|---|---|
| Falcon | 7B / 40B / 180B / Falcon3 / H1 | MQA、多语言、Falcon-H1 混合 | TII Falcon License | 阿联酋 TII |
| MPT | 7B / 30B | ALiBi、无位置 embedding、长上下文 | Apache 2.0 | MosaicML |
| BLOOM | 176B | 70 层、14336、112 头、ALiBi、多语言 | BigScience RAIL | 协作项目 |
| GPT-NeoX | 20B | 44 层、6144、64 头、RoPE | Apache 2.0 | EleutherAI |
| Pythia | 70M–12B | 小到大一套、公开训练顺序 | Apache 2.0 | 可复现研究 |
| OLMo | 1B–32B | 全开放数据/代码/训练 | Apache 2.0 | AI2 |
| DCLM | 7B | 公开数据筛选、dense | 自定义/开放 | 数据研究 |
| Nemotron | 8B–70B / Nemotron-H | dense + hybrid Mamba | NVIDIA 许可 | 英伟达 |
| Granite | 3.x/4.x | dense + hybrid、企业向 | Apache 2.0 | IBM |
| DBRX | 132B | 16 专家 top-4、36B 激活 | Databricks License | 企业 MoE |
| Arctic | 480B | 128 专家 top-2、17B 激活 | Apache 2.0 | Snowflake |
| Command R | 35B / R+ 104B | dense、128K、工具调用 | CC-BY-NC | Cohere |
| Grok-1 | 314B | 8 专家 top-2、8K | Apache 2.0 | xAI 开放权重 |

> 这张表是“代表”，不是“全部”。同一家族还有大量尺寸、微调、量化版本；附录给更完整的索引。

## 8.2 Falcon：MQA 与多语言

Falcon 7B 的结构很特别：32 层、4544 hidden、71 个 Q 头，但 K/V 头远少于 Q 头（MQA 思路）。这让 KV cache 很小，适合高并发；代价是 K/V 表达被压缩，长上下文精细检索弱。

Falcon 40B：60 层、8192 hidden、128 个 Q 头；Falcon 180B：80 层、14848 hidden、232 个 Q 头。Falcon3 系列把尺寸拉到 1B–40B，改用 GQA、RoPE、128K 上下文；Falcon-H1 则是 Mamba/Transformer 混合，44 层、3072 hidden、12 Q/2 KV、262K。

## 8.3 BLOOM：超大 dense 的历史样本

BLOOM 176B：70 层、14336 hidden、112 个 Q 头、2048 上下文、ALiBi 位置偏置、46 种语言。它是 2022 年最大的开放多语言模型之一，训练数据/代码/协作过程都公开，许可证是 RAIL（有使用限制）。

KV 账（MHA，head_dim 128，FP16）：

$$
2\times70\times112\times128\times2
=4{,}014{,}080\ \text{bytes/token}
\approx3.83\ \text{MiB/token}
$$

2048 上下文约 7.7 GiB。对 176B 权重（FP16 约 352GB）来说，KV 不是最大问题；权重才是。

## 8.4 MPT：ALiBi 长上下文

MPT-7B：32 层、4096 hidden、32 个 Q 头、2048 上下文；MPT-30B：48 层、7168 hidden、64 个 Q 头、8K。它用 ALiBi 而不是 RoPE：给注意力头加一个与距离成线性的偏置，训练短、外推长。

MPT 的工程意义大于架构意义：它是早期用开源训练栈（Composer）大规模训练的代表，证明“不用 RoPE 也能做长上下文”。

## 8.5 OLMo / Pythia / DCLM：开放数据三兄弟

| 模型 | 开放什么 | 架构 | 为什么重要 |
|---|---|---|---|
| OLMo 2 7B | 数据、代码、训练日志、checkpoint | 32 层、4096、32/32、4K | 真正可复现的训练 |
| OLMo 3 32B | 同上，规模更大 | 64 层、5120、40/8、64K YaRN | 开放模型的质量上限 |
| Pythia 12B | 训练顺序、数据去重版 | 36 层、5120、40 头、2K | 研究缩放/记忆 |
| DCLM 7B | 数据筛选管线 | 32 层、4096、32 头、2K/8K | 数据质量研究 |

> 如果你要研究“数据配比对模型的影响”，OLMo/Pythia/DCLM 比 Llama 更有价值；Llama 只给权重，不给数据。

## 8.6 DBRX / Arctic / Grok-1：MoE 的三种写法

| 模型 | 总参/激活 | 层数 | hidden | 专家 | top-k | 上下文 |
|---|---|---|---|---|---|---|
| DBRX | 132B / 36B | 40 | 6144 | 16 | 4 | 32K |
| Arctic | 480B / 17B | 80? | 7168? | 128 | 2 | 32K |
| Grok-1 | 314B / ? | 64 | 6144 | 8 | 2 | 8K |

DBRX 是“少专家、宽专家、top-4”，偏企业单机/多机；Arctic 是“多专家、top-2”，激活极低但总参数大；Grok-1 是“8 专家 top-2”，更接近早期 Mixtral 思路。三者的路由策略不同，不能只看“都是 MoE”。

> Arctic 的部分层数/宽度在公开模型卡里写法不一，表中标 `?` 的字段不要当精确值；读具体 config 为准。

## 8.7 Command R 与许可证陷阱

Command R 35B、Command R+ 104B 是 Cohere 的开放权重模型，支持 128K、工具调用、RAG。它们的许可证是 CC-BY-NC 4.0：**可以研究、可以改、不能商用**。很多团队下载后直接上线，违反许可。

> 选型时先问“商用吗？”再问“多大？”。许可证错，模型再好也不能用。

## 8.8 手算：BLOOM vs MPT 的 KV

MPT-7B：32 层、32 KV、head_dim 128、FP16：

$$
2\times32\times32\times128\times2=524{,}288\ \text{bytes/token}=0.5\ \text{MiB/token}
$$

2048 上下文约 1 GiB。

BLOOM 176B 每 token 3.83 MiB，是 MPT 的 7.6 倍。**大 dense + 多 KV 头 = KV 灾难；这就是 GQA/MQA 后来成为默认的原因。**

## 8.9 常见误解

- **“BLOOM 是开源模型，所以能随便商用。”** RAIL 有使用限制，不是 Apache。
- **“MPT 用 ALiBi 就一定比 RoPE 长。”** 外推行为不同，实际长上下文还要看训练长度和数据。
- **“OLMo 只是另一个 7B。”** 它的价值在数据/代码/日志全开放，架构不是重点。
- **“Command R 是 Apache。”** 它是 CC-BY-NC，不能商用。

## 8.10 自测

1. Falcon 7B 的 Q 头数和 KV 策略有什么特别？
2. BLOOM 176B 的层数、hidden、头数、上下文各是多少？
3. OLMo 与 Llama 最大的差别是什么？
4. DBRX、Arctic、Grok-1 的专家数和 top-k 各是多少？
5. Command R+ 的许可证是什么？商用需要做什么？

> 参考答案：1）71 个 Q 头，K/V 头远少于 Q（MQA 思路）；2）70 层、14336、112 头、2048；3）OLMo 开放数据/代码/训练日志，Llama 只开放权重；4）DBRX 16/top-4，Arctic 128/top-2，Grok-1 8/top-2；5）CC-BY-NC 4.0，商用需另获授权。

## 8.11 复习锚点

- Falcon：MQA、多语言、Falcon-H1 混合。
- BLOOM：70/14336/112/2048、RAIL。
- MPT：ALiBi、长上下文。
- OLMo/Pythia/DCLM：开放数据。
- DBRX/Arctic/Grok-1：MoE 三种路由。
- Command R：非商用许可。
- 下一章：中国开放权重，从 GLM 到 Kimi、MiniMax、InternLM。
