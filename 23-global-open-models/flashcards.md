# 抽认卡

## f01 · 开放权重 vs 开源

权重可下载 ≠ 代码/数据/商用权利都开放

## f02 · 判断顺序

许可证 → 权重 → 代码 → 数据

## f03 · 本册口径

官方公开、可下载权重、主要家族；不逐 checkpoint

## f04 · 六旋钮

注意力、FFN、归一化、位置、激活、模态

## f05 · 六骨架

dense、MoE、encoder-decoder、线性/SSM、多模态、扩散

## f06 · 读卡六维

骨架、规模、注意力、FFN、上下文、许可证

## f07 · Llama 1 默认值

RoPE、SwiGLU、RMSNorm、decoder-only

## f08 · Llama 4 激活

Scout 17B/109B，Maverick 17B/400B

## f09 · Llama 3.3 70B KV

0.3125 MiB/token；128K≈40 GiB

## f10 · Qwen 三条路线

小 dense、大 MoE、混合线性

## f11 · Qwen3.8-2.4T

92 层、8192、512 专家 top-10、262K

## f12 · Qwen3.8-27B KV

0.25 MiB/token；262K≈64 GiB

## f13 · Mistral 7B

32 层、4096、GQA 8 KV、滑窗 4096

## f14 · Mixtral 8x7B

46.7B 总 / 12.9B 激活，8 专家 top-2

## f15 · Mistral Small 4

36 层、32/32 KV、128 专家 top-4、1M

## f16 · Gemma 3

5:1 局部/全局、QK-Norm、128K

## f17 · Gemma 4 12B

48 层、3840、16/8、262K、any-to-any

## f18 · Gemma 3 27B KV

16 KV、128 维；128K≈62 GiB

## f19 · Phi-4

40 层、5120、40/10、16K、14B

## f20 · Phi-4-mini

32 层、3072、24/8、128K、3.8B

## f21 · Phi 核心

数据课程 + 小模型 + 长训练

## f22 · Falcon

MQA、多语言；H1 混合

## f23 · BLOOM

70 层、14336、112 头、2048

## f24 · OLMo

开放数据/代码/日志

## f25 · GLM-5.3

78 层、6144、64/64、256 专家 top-8、1M

## f26 · Kimi K3

93 层、7168、96/96、896 专家、1M

## f27 · MiniMax M3

60 层、6144、64/4、top-4+1、1M

## f28 · SSM

h_t=A h_{t-1}+B x_t；y_t=C h_t

## f29 · Jamba

Transformer + Mamba 混合

## f30 · 混合注意力

大部分线性 + 少量全注意力

## f31 · 总参/激活

总参=显存；激活=每 token 算力

## f32 · Qwen3.8-2.4T

2.4T 总 / 95B 激活，512 专家 top-10

## f33 · 共享专家

所有 token 都走，学通用能力

## f34 · 图像 token

448/14=32，32²=1024；2×2 合并=256

## f35 · 多模态三段式

ViT → 连接器 → LLM

## f36 · Janus

理解头 + 生成头双系统

## f37 · GQA 公式

2 × L × H_kv × d_head × b

## f38 · 1M KV

朴素可达数百 GiB，必须稀疏/压缩

## f39 · YaRN

factor 外推倍数；original 原训练长度

## f40 · 许可证

Apache/MIT 宽松；Llama/Gemma 有条件；CC-BY-NC 禁商用

## f41 · 开放数据

OLMo/Pythia/DCLM 可复现

## f42 · 污染检测

改写题目/换数字重测

## f43 · config 字段

architectures/model_type/层数/hidden/QKV/专家/上下文

## f44 · MoE 参数估算

E × 3 × H × F_exp × L

## f45 · KV 估算

2 × L × H_kv × d_head × b

## f46 · 选型顺序

许可证 → 显存 → 上下文 → 任务

## f47 · MoE 显存

按总参数，不按激活参数

## f48 · 索引口径

家族级，不逐 checkpoint
