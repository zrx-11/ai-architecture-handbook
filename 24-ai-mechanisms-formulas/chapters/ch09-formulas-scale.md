# 第 9 章：规模、成本与对齐公式（44–75）

这一组公式开始和钱、卡、时间、人类偏好打交道。它们不再是“模型内部形状”，而是“这件事值不值”。

## 一句话核心

规模公式估预算，对齐公式估偏好；两者都不能脱离数据分布和实测 MFU。

## 学习目标

- 能用缩放定律与 Chinchilla 配比估训练预算。
- 能算训练/推理显存、通信量、每百万 token 成本。
- 能区分 RLHF、DPO、GRPO 的目标函数与数据需求。

## 公式清单

### 44. 缩放定律

$$
L(N,D)\approx E+\frac{A}{N^\alpha}+\frac{B}{D^\beta}
$$

用途：给定算力估 loss。易错：常数依数据分布而变，换语料外推会偏；它预测 loss，不预测能力。

### 45. Chinchilla 配比

$$
D_{\text{opt}}\approx20N
$$

用途：给定算力配参数与 token。易错：那是“给定算力最优”，推理量大时反而该小模型多训数据。

### 46. 训练显存

$$
\text{字节/参数}\approx16
$$

用途：选卡、定并行前必算。易错：还要另加激活；长上下文时激活常是最大一块。

### 47. 推理显存

$$
\text{显存}\approx N\times\text{每参数字节}+\text{KV cache}
$$

用途：估能开多大上下文、多少并发。易错：只算权重忘 KV，长上下文部署必爆。

### 48. KV cache

$$
\text{KV}=2\times L\times n_{kv}\times d_{\text{head}}\times\text{bytes}\times\text{seq}\times\text{batch}
$$

用途：任何自回归推理都要算。易错：系数 2 是 K 和 V，最常漏；还要乘并发。

### 49. FLOPs 估算

$$
\text{训练}\approx6ND,\quad \text{推理}\approx2N\times\text{tokens}
$$

用途：估训练时间与算力。易错：6ND 漏了注意力二次项；真实 MFU 只有 35%–45%。

### 50. 数据并行通信量

$$
\text{通信量}\approx2\times\frac{N-1}{N}\times\text{参数量}\times\text{字节数}
$$

用途：判断能不能纯 DP。易错：超过机内带宽就只能上 TP/PP。

### 51. 算术强度

$$
\text{算术强度}=\frac{\text{FLOPs}}{\text{字节数}},\quad
\text{硬件拐点}=\frac{\text{峰值算力}}{\text{带宽}}
$$

用途：判断卡算力还是卡带宽。易错：decode 算术强度约 1–2，远低于拐点。

### 52. 每百万 token 成本

$$
\text{成本}=\frac{\text{输入 token}\times\text{单价}_{in}+\text{输出 token}\times\text{单价}_{out}}{10^6}
$$

用途：预算与选型。易错：缓存命中、重试、工具轮次都计费，账单价不等于真实成本。

### 53. 训练时间估算

$$
\text{时间}\approx\frac{6ND}{\text{卡数}\times\text{单卡算力}\times\text{MFU}}
$$

用途：排期与申请资源。易错：MFU 是最大变量，标称峰值通常含稀疏加速。

### 54. decode 带宽需求

$$
\text{带宽}\approx\frac{\text{参数量}\times\text{字节数}}{\text{TPOT}}
$$

用途：判断单卡能否达到目标 TPOT。易错：批处理能让多个请求共享一次读取，并发越高摊薄越明显。

### 55. Amdahl 定律

$$
\text{加速比}=\frac{1}{(1-p)+p/s}
$$

用途：决定优化优先级。易错：只优化占比 10% 的部分，收益上限只有 1.1 倍。

### 56. 电力与碳成本

$$
\text{成本}=\text{功率}\times\text{小时}\times\text{电价},\quad
\text{碳排}=\text{电量}\times\text{碳强度}
$$

用途：总拥有成本与碳核算。易错：只算 GPU 功耗，漏掉网络与冷却，PUE 常差两成。

### 57. 并行度上限

$$
\text{有效加速比}=\frac{N}{1+N(1-\eta)/\eta}
$$

用途：规划集群规模。易错：线性外推“卡翻倍时间减半”，几百卡后通信吃掉收益。

### 58. MoE 的 all-to-all 通信量

$$
\text{通信量}\approx2\times\text{tokens}\times d\times\text{字节数}
$$

用途：判断专家能否跨机。易错：只算参数不算通信，专家并行做不好会被 all-to-all 吃光。

### 59. prefill 与 decode 的算力比

$$
\text{prefill}=2NL_{\text{prompt}},\quad
\text{decode}=2NL_{\text{out}}
$$

用途：判断长提示贵在哪。易错：长提示的开销主要在 prefill，不是 decode。

### 60. KL 散度

$$
D_{\mathrm{KL}}(p\|q)=\sum_x p(x)\log\frac{p(x)}{q(x)}
$$

用途：偏好优化里约束“别跑太远”。易错：KL 不对称，方向选错惩罚的东西就变了。

### 61. RLHF 目标

$$
\max\ \mathbb E[r_\theta(x,y)]-\beta D_{\mathrm{KL}}(\pi\|\pi_{\text{ref}})
$$

用途：奖励模型 + KL 缰绳。易错：$\beta$ 太小会奖励黑客，太大又学不到东西。

### 62. Bradley-Terry 偏好模型

$$
P(y_w\succ y_l)=\sigma(r(y_w)-r(y_l))
$$

用途：把成对比较转成标量奖励。易错：它假设标注无噪声，前后矛盾会被当信号学进去。

### 63. PPO 裁剪目标

$$
L=\min\left(r_t\hat A_t,\ \operatorname{clip}(r_t,1-\varepsilon,1+\varepsilon)\hat A_t\right)
$$

用途：在线策略优化。易错：它只限单步，不限总方向，还要 KL 或早停兜底。

### 64. DPO 损失

$$
-\log\sigma\left(\beta\left[\log\frac{\pi(y_w)}{\pi_{\text{ref}}(y_w)}-\log\frac{\pi(y_l)}{\pi_{\text{ref}}(y_l)}\right]\right)
$$

用途：固定偏好数据直接优化。易错：DPO 的 $\beta$ 语义与 RLHF 相反，越大越激进。

### 65. GRPO

$$
\hat A_i=\frac{r_i-\operatorname{mean}(r_1,\ldots,r_G)}{\operatorname{std}(r_1,\ldots,r_G)}
$$

用途：可验证任务做 RLVR，省掉价值网络。易错：组内方差太小（全对或全错）时优势接近 0。

### 66. 逐 token 的 KL 惩罚

$$
\mathrm{KL}_t=\log\pi(y_t\mid\cdot)-\log\pi_{\text{ref}}(y_t\mid\cdot)
$$

用途：RLHF 的逐 token 记账。易错：总和随长度线性涨，跨长度比较要用每 token 均值。

### 67. 拒绝采样

$$
D=\{(x,y_{k^*})\mid k^*=\arg\max_k r(x,y_k)\}
$$

用途：采多条、按奖励挑最好做训练数据。易错：它只抬高分布尾巴，不创造新能力。

### 68. GAE 优势估计

$$
A_t=\sum_{k\ge0}(\gamma\lambda)^k\delta_{t+k}
$$

用途：PPO 里估优势。易错：$\lambda$ 与 $\gamma$ 一起决定视野，单独调一个容易失衡。

### 69. 奖励模型一致性

$$
\text{一致率}=\frac{\text{与人类同序的对数}}{\text{总对数}}
$$

用途：判断奖励模型能不能信。易错：低于 0.6 说明标注本身有歧义，不是模型不够大。

### 70. KL 预算与熔断

$$
\text{累积 KL}=\sum_t \mathrm{KL}(\pi_t\|\pi_{\text{ref}})
$$

用途：长时间 RL 的熔断器。易错：用总和跨实验比较没意义，长度不同不可比。

### 71. 拒绝采样通过率

$$
P(\text{至少一条正确})=1-(1-p)^n
$$

用途：估算采多少条才够。易错：成本随 $n$ 线性涨，收益递减。

### 72. SFT 数据量

$$
\text{所需条数}\approx1\text{k（格式）到 }100\text{k（领域注入）}
$$

用途：决定指令微调规模。易错：不是越多越好，重复风格只会让输出更单调。

### 73. 偏好数据量

$$
\text{每类任务约 }1\text{k–}10\text{k 对}
$$

用途：准备偏好数据配比。易错：质量比数量重要，一致性低于 0.6 会教坏奖励模型。

### 74. RL 采样预算

$$
\text{rollouts}=\text{prompts}\times G\times\text{epochs}
$$

用途：估 RL 训练成本。易错：大头在采样，不在梯度更新；只算训练步数会严重低估。

### 75. 奖励模型的方差

$$
\text{估计方差}\propto\frac1{\sqrt n}
$$

用途：规划标注预算。易错：加倍数据只降约 30% 误差，突破不了标注一致性上限。

## 常见误解

- “Chinchilla 配比适用于所有模型。”推理成本高时，小模型多训数据更划算。
- “MFU 可以按标称算。”真实值常 30%–50%，还随模型与并行策略变化。
- “奖励模型 loss 低就能用。”先看与人类排序的一致率。

## 自测

1. 70B、bf16、1.4T token，训练 FLOPs 约多少？
2. 8K 上下文、batch 16 的 Llama-3-8B，KV 约多少？
3. GRPO 组内全对时，为什么这一批采样白费？

## 复习锚点

- 规模看 6ND、20N、16 字节/参数。
- 对齐看数据形态与 KL 缰绳。
- 成本看单位与口径，不看单价标签。

## 来源

<https://mp.weixin.qq.com/s/5J2KoDfP7FFfS6ojHmxuAw>
