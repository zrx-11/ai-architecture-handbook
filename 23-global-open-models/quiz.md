# 测验题库

共 53 题，按章节排列。


## ch01

**q01** “开放权重”最准确的含义是？

- A. 模型参数可下载
- B. 训练数据公开
- C. 训练代码公开
- D. 许可证允许商用
- 答案：A
- 解析：开放权重只承诺参数可获取；代码、数据、商用权利要另看。

**q02** Apache 2.0 与 CC-BY-NC 最关键的区别是？

- A. 前者允许商用，后者禁止商用
- B. 前者禁止修改，后者允许
- C. 两者都禁止商用
- D. 前者只允许研究
- 答案：A
- 解析：Apache 2.0 允许商用；CC-BY-NC 的 NC 就是非商用。

**q03** 本册为什么按“家族”而不是按每个 checkpoint 组织？

- A. checkpoint 数量无穷且架构重复
- B. 家族名字更好听
- C. 每个 checkpoint 都有独立架构
- D. Hugging Face 不支持 checkpoint
- 答案：A
- 解析：量化/微调/合并版大量重复，家族级才能建立结构感。


## ch02

**q04** 下列哪一项不是本章说的“结构旋钮”？

- A. 学习率
- B. 注意力类型
- C. FFN 类型
- D. 位置编码
- 答案：A
- 解析：学习率是训练超参，不是模型结构。

**q05** MoE 的“总参数”和“激活参数”分别决定什么？

- A. 显存 / 每 token 算力
- B. 算力 / 显存
- C. 都决定显存
- D. 都决定算力
- 答案：A
- 解析：总参数要全装，决定显存；激活参数决定每 token 计算量。

**q06** 线性注意力主要解决什么问题？

- A. 长序列的二次复杂度
- B. 词表太小
- C. 多模态编码
- D. 许可证问题
- 答案：A
- 解析：它把注意力复杂度从 O(n^2) 降到 O(n)，代价是状态容量有限。


## ch03

**q07** Llama 1 定下的四个结构默认值不包括？

- A. MoE 路由
- B. RoPE
- C. SwiGLU
- D. RMSNorm
- 答案：A
- 解析：Llama 1 是 dense，没有 MoE。

**q08** Llama 2 70B 用 GQA 主要省哪部分显存？

- A. KV cache
- B. 词表 embedding
- C. FFN 权重
- D. 输出头
- 答案：A
- 解析：64 个 Q 头共享 8 组 K/V，KV cache 降到 MHA 的 1/8。

**q09** Llama 4 Scout 的“17B”指什么？

- A. 每 token 激活参数
- B. 总参数
- C. 专家数
- D. 上下文长度
- 答案：A
- 解析：Scout 总参数约 109B，17B 是激活参数。

**q10** Llama 3.3 70B 在 128K 下单序列 KV 约多少？

- A. 40 GiB
- B. 4 GiB
- C. 140 GiB
- D. 400 GiB
- 答案：A
- 解析：0.3125 MiB/token × 131072 ≈ 40 GiB。


## ch04

**q11** Qwen3.8-2.4T-A95B 的 95B 指什么？

- A. 每 token 激活参数
- B. 总参数
- C. 专家数
- D. KV 头数
- 答案：A
- 解析：A95B 的 A 是 active；2.4T 是总参数。

**q12** Qwen3.5-397B-A17B 的专家数和 top-k 是？

- A. 512 / 10
- B. 256 / 8
- C. 128 / 8
- D. 896 / 8
- 答案：A
- 解析：config：512 专家，top-10，专家宽度 1024。

**q13** Qwen3.8-27B 的 KV 头数和 head_dim 是？

- A. 4 / 256
- B. 8 / 128
- C. 16 / 128
- D. 32 / 256
- 答案：A
- 解析：text_config：4 个 KV 头，head_dim 256。

**q14** Qwen 的三条子路线不包括？

- A. encoder-decoder
- B. 小尺寸 dense
- C. 大尺寸 MoE
- D. 混合线性注意力
- 答案：A
- 解析：Qwen 主线是 decoder-only；encoder-decoder 不是它的子路线。


## ch05

**q15** Mistral 7B 的滑窗大小是？

- A. 4096
- B. 1024
- C. 32768
- D. 128
- 答案：A
- 解析：Mistral 7B 用 4096 滑动窗口，最大位置 32K。

**q16** Mixtral 8x7B 的总参数 / 激活参数约是？

- A. 46.7B / 12.9B
- B. 56B / 56B
- C. 12.9B / 46.7B
- D. 141B / 39B
- 答案：A
- 解析：8 个专家都装，top-2 只算 2 个。

**q17** Mistral Small 4 119B 的 KV 头数是？

- A. 32
- B. 4
- C. 8
- D. 64
- 答案：A
- 解析：config：32 Q/32 KV，是 MHA，不是 GQA。


## ch06

**q18** Gemma 3 的局部/全局比例是？

- A. 5:1
- B. 1:1
- C. 1:5
- D. 全局部
- 答案：A
- 解析：每 6 层 5 层局部、1 层全局；Gemma 2 约 1:1。

**q19** QK-Norm 主要解决什么问题？

- A. 大 head_dim 下 attention logits 爆炸
- B. 词表太大
- C. 专家不均衡
- D. KV 头太少
- 答案：A
- 解析：对 Q/K 归一化，稳定长上下文训练。

**q20** Gemma 4 12B 的架构特点是？

- A. 统一 any-to-any
- B. 纯文本 dense
- C. 8 专家 MoE
- D. 纯 SSM
- 答案：A
- 解析：Gemma4Unified 处理文/图/音，262K。


## ch07

**q21** Phi-4 14B 的层数、hidden、Q/KV 是？

- A. 40 / 5120 / 40 / 10
- B. 32 / 3072 / 32 / 32
- C. 48 / 4096 / 32 / 8
- D. 62 / 5376 / 32 / 16
- 答案：A
- 解析：Phi-4：40 层、5120、40 Q/10 KV、16K。

**q22** Phi-4-mini 在 128K 下单序列 KV 约多少？

- A. 16 GiB
- B. 4 GiB
- C. 64 GiB
- D. 1 GiB
- 答案：A
- 解析：32 层×8 KV×128 维×2 字节×2=0.125 MiB/token，128K≈16 GiB。

**q23** Phi 系列最核心的竞争力是？

- A. 数据课程与小模型训练
- B. MoE 路由
- C. 线性注意力
- D. 多模态生成
- 答案：A
- 解析：结构基本是 Llama 式；数据和训练配方是差异。


## ch08

**q24** BLOOM 176B 的层数、hidden、头数是？

- A. 70 / 14336 / 112
- B. 80 / 8192 / 64
- C. 32 / 4096 / 32
- D. 60 / 6144 / 48
- 答案：A
- 解析：BLOOM 176B：70 层、14336、112 头、2048 上下文。

**q25** OLMo 与 Llama 最大的差别是？

- A. OLMo 开放数据/代码/训练日志
- B. OLMo 没有注意力
- C. OLMo 是 MoE
- D. OLMo 不能商用
- 答案：A
- 解析：OLMo 是全开放研究线；Llama 主要开放权重。

**q26** Command R+ 的许可证是？

- A. CC-BY-NC 4.0
- B. Apache 2.0
- C. MIT
- D. Llama Community
- 答案：A
- 解析：CC-BY-NC 禁止商用，商用需另获授权。


## ch09

**q27** GLM-5.3 的 model_type 是？

- A. glm_moe_dsa
- B. llama
- C. mixtral
- D. kimi_linear
- 答案：A
- 解析：MoE + DSA 稀疏注意力；78 层、6144、64/64、256 专家 top-8。

**q28** Kimi K3 的专家数是？

- A. 896
- B. 128
- C. 256
- D. 512
- 答案：A
- 解析：config：896 专家，93 层、7168、96/96、1M。

**q29** MiniMax M3 的 4 个 KV 头 + 1M 上下文说明什么？

- A. 朴素 KV 约 240 GiB，必须稀疏/压缩
- B. 它不需要 KV
- C. 它是 dense
- D. 它只有 4 层
- 答案：A
- 解析：2×60×4×128×2=0.234 MiB/token，1M≈240 GiB。

**q30** Intern-S2 的 text model_type 是？

- A. qwen3_5_moe_text
- B. llama
- C. glm_moe_dsa
- D. step5
- 答案：A
- 解析：它复用 Qwen3.5 MoE 骨架，做多模态/数据创新。


## ch10

**q31** SSM 的递推式是？

- A. h_t = A h_{t-1} + B x_t
- B. h_t = QK^T V
- C. h_t = softmax(x)
- D. h_t = W x + b
- 答案：A
- 解析：状态递推，输出 y_t=C h_t；状态维度固定。

**q32** Jamba 的架构是？

- A. Transformer + Mamba 混合
- B. 纯 SSM
- C. 纯 RNN
- D. 纯 CNN
- 答案：A
- 解析：混合架构，保留部分注意力。

**q33** Kimi K3 与 Qwen3-Next 的共同点是？

- A. 线性/混合注意力 + MoE
- B. 都是 dense
- C. 都是 encoder-decoder
- D. 都没有专家
- 答案：A
- 解析：大部分层线性、少量全注意力，外加 MoE。


## ch11

**q34** “2.4T-A95B”最准确读法是？

- A. 总参数 2.4T，每 token 激活 95B
- B. 总参数 95B，激活 2.4T
- C. 两者都是总参数
- D. 两者都是激活参数
- 答案：A
- 解析：A 是 active，总参数和激活参数分开。

**q35** Qwen3.8-2.4T 的专家数、top-k、专家宽度是？

- A. 512 / 10 / 2048
- B. 256 / 8 / 1024
- C. 128 / 8 / 1536
- D. 896 / 8 / 3072
- 答案：A
- 解析：config：512 专家、top-10、moe_intermediate 2048。

**q36** 共享专家的主要作用是？

- A. 承担通用能力，缓解路由碎片化
- B. 增加路由层数
- C. 替代 KV cache
- D. 减少词表
- 答案：A
- 解析：所有 token 都走共享专家，学通用知识。

**q37** Mixtral 8x7B 每 token 激活约多少？

- A. 12.9B
- B. 46.7B
- C. 7B
- D. 56B
- 答案：A
- 解析：top-2 专家 + 注意力/embedding，约 12.9B。


## ch12

**q38** 448×448 图像、patch 14，token 数是多少？

- A. 1024
- B. 256
- C. 512
- D. 4096
- 答案：A
- 解析：(448/14)^2=32^2=1024；2×2 合并后 256。

**q39** 图像 token 对 KV cache 的影响是？

- A. 和文本 token 一样占 KV
- B. 完全不占
- C. 只占权重
- D. 只占词表
- 答案：A
- 解析：图像 token 进同一序列、同一 KV。

**q40** Janus 的双系统是指？

- A. 理解头 + 生成头
- B. 文本头 + 音频头
- C. 编码器 + 解码器
- D. MoE + dense
- 答案：A
- 解析：理解与生成解耦，避免目标冲突。


## ch13

**q41** GQA 的 KV/token/layer 公式是？

- A. 2 × H_kv × d_head × b
- B. 2 × H × d_head × b
- C. H × d_head × b
- D. 2 × L × H × b
- 答案：A
- 解析：只有 KV 头数参与；H_kv 是组数。

**q42** Llama 3.3 70B 在 32K 下单序列 KV 约多少？

- A. 10 GiB
- B. 40 GiB
- C. 4 GiB
- D. 100 GiB
- 答案：A
- 解析：0.3125 MiB × 32768 ≈ 10 GiB。

**q43** 1M 上下文模型为什么必须稀疏/压缩？

- A. 朴素 KV 可达数百 GiB
- B. 因为词表太大
- C. 因为层数太少
- D. 因为不能用 GPU
- 答案：A
- 解析：例如 MiniMax M3 朴素 KV 约 240 GiB。

**q44** YaRN 的 factor 表示什么？

- A. 长度外推倍数
- B. KV 头数
- C. 专家数
- D. 学习率
- 答案：A
- 解析：factor=8 把 8K 训练长度外推到 64K 量级。


## ch14

**q45** CC-BY-NC 的核心限制是？

- A. 禁止商用
- B. 禁止修改
- C. 禁止再分发
- D. 禁止研究
- 答案：A
- 解析：NC = NonCommercial；研究可以，商用要授权。

**q46** OLMo 比 Llama 更适合训练复现，因为？

- A. 开放数据/代码/日志
- B. 参数更大
- C. 没有注意力
- D. 许可证更严
- 答案：A
- 解析：OLMo 是全开放研究线。

**q47** 检测 benchmark 污染的可行方法是？

- A. 改写题目/换数字重测
- B. 只看排行榜
- C. 只看模型大小
- D. 只跑一个样本
- 答案：A
- 解析：改写后分数大跌说明可能靠记忆。


## ch15

**q48** `architectures` 和 `model_type` 的区别是？

- A. 前者是类名，后者是配置族
- B. 两者完全一样
- C. 前者是许可证
- D. 后者是参数量
- 答案：A
- 解析：`LlamaForCausalLM` vs `llama`。

**q49** `num_experts` 和 `num_experts_per_tok` 的区别是？

- A. 总专家数 / top-k
- B. top-k / 总专家数
- C. 层数 / 头数
- D. 词表 / 上下文
- 答案：A
- 解析：前者是全部专家，后者是每 token 选几个。

**q50** Qwen3.8-2.4T 的 95B 激活大致来自？

- A. top-10 专家 + 注意力/embedding
- B. 全部 512 专家
- C. 只 embedding
- D. 只 KV cache
- 答案：A
- 解析：10 个专家×92 层≈46B，加注意力/embedding 到 95B。


## ch16

**q51** 本索引的收录口径是？

- A. 官方公开、可下载权重的主要家族
- B. 所有微调/量化 checkpoint
- C. 所有论文
- D. 所有 API 模型
- 答案：A
- 解析：家族级，不逐 checkpoint。

**q52** MoE 权重显存按哪个参数估？

- A. 总参数
- B. 激活参数
- C. KV 头数
- D. 词表
- 答案：A
- 解析：全部专家都要装，按总参数；算力按激活。

**q53** 选型的正确顺序是？

- A. 许可证 → 显存 → 上下文 → 任务
- B. 参数 → 名字 → 排行榜
- C. 价格 → 颜色 → 品牌
- D. 上下文 → 许可证 → 参数量
- 答案：A
- 解析：许可证不合格直接排除；再算显存/上下文。
