# 第 10 章：生成、效率与推理公式（76–104）

最后一组公式把生成模型的采样、量化、LoRA、投机解码、服务容量串起来。它们的共同点是：分子是收益，分母是成本。

## 一句话核心

生成公式看采样步数与引导强度，效率公式看带宽与位宽，服务公式看延迟与并发。

## 学习目标

- 能解释扩散前向、CFG、VAE ELBO、GAN 目标各自在优化什么。
- 能算 LoRA 参数量、量化显存、投机解码加速比。
- 能用 Little 定律与 TTFT/TPOT 做容量规划。

## 公式清单

### 76. 扩散前向

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\varepsilon
$$

用途：训练时按任意 $t$ 一步加噪。易错：训练侧噪声表常 1000 步，采样只用 20–50 步，两个 $T$ 不是一回事。

### 77. 扩散训练目标

$$
L=\mathbb E\|\varepsilon-\varepsilon_\theta(x_t,t)\|^2
$$

用途：预测加进去的噪声，训练更稳。易错：预测 $\varepsilon$ 与预测 $x_0$ 数学等价，但数值稳定性差很多。

### 78. CFG

$$
\hat\varepsilon=\varepsilon_{\text{uncond}}+s(\varepsilon_{\text{cond}}-\varepsilon_{\text{uncond}})
$$

用途：放大提示词影响。易错：$s$ 常取 3–7，太大过饱和、多样性塌陷。

### 79. VAE 的 ELBO

$$
\log p(x)\ge\mathbb E_q[\log p(x\mid z)]-\mathrm{KL}(q(z\mid x)\|p(z))
$$

用途：训练 VAE、给扩散准备隐空间。易错：加大 KL 权重会更规整但重建更糊，这是设计取舍。

### 80. GAN 目标

$$
\min_G\max_D\ \mathbb E[\log D(x)]+\mathbb E[\log(1-D(G(z)))]
$$

用途：极快采样与窄场景。易错：理论最优假设判别器最优，实践中做不到，所以训练不稳。

### 81. 温度与 top-p 采样

$$
p_i=\operatorname{softmax}(z_i/T),\quad \text{按累积概率截断}
$$

用途：控制生成保守/发散。易错：温度与 top-p 会互相作用，低温下 top-p 容易截掉太多候选。

### 82. 扩散采样步数

$$
\text{质量}\approx f(\text{步数}),\quad \text{收益递减}
$$

用途：决定生成速度与质量取舍。易错：步数与 CFG 要一起调，CFG 高时步数太少会出硬边。

### 83. CFG 的多样性代价

$$
s\uparrow\Rightarrow\text{提示贴合}\uparrow,\ \text{模式覆盖}\downarrow
$$

用途：批量出图时判断要不要降 $s$。易错：$s$ 从 3 提到 7，独特构图数可能减半。

### 84. 图像 latent 压缩比

$$
\text{压缩比}=\frac{H\times W}{h\times w}
$$

用途：设计生成管线，估算力。易错：压缩比越高越省，但细节越差，16 倍下采样画不出小字。

### 85. CFG 的计算成本

$$
\text{成本}\approx2\times\text{单次前向}
$$

用途：低延迟场景权衡。易错：CFG 一直是双倍算力，$s=0$ 才能省一半。

### 86. 扩散的信噪比

$$
\mathrm{SNR}(t)=\frac{\bar\alpha_t}{1-\bar\alpha_t}
$$

用途：设计噪声表、排查哪一步出问题。易错：每步去噪难度差几个数量级，一步采样难以奏效。

### 87. 对称量化

$$
s=\frac{\max|w|}{q},\quad \hat w=\operatorname{round}(w/s)
$$

用途：部署压显存与带宽。易错：逐张量缩放在分布不均时精度掉得厉害，要逐组 32–128。

### 88. LoRA

$$
W'=W+BA,\quad B\in\mathbb R^{d\times r},\ A\in\mathbb R^{r\times k}
$$

用途：低秩微调，显存有限时用。易错：$A$ 高斯初始化、$B$ 初始化为零，反了起点就偏。

### 89. 蒸馏

$$
L=(1-\alpha)\mathrm{CE}(y,p_s)+\alpha T^2\mathrm{KL}(p_t^T\|p_s^T)
$$

用途：大模型能力压到小模型。易错：$T^2$ 是让梯度量级与温度无关，漏了每次改 $T$ 都要重调学习率。

### 90. 推测解码加速比

$$
\text{加速比}\approx\frac{1-\alpha^{\gamma+1}}{(1-\alpha)(1+c\gamma)}
$$

用途：带宽受限、延迟敏感时估收益。易错：接受率随温度下降，高温时可能比不开还慢。

### 91. FlashAttention 显存

$$
\text{显存 }O(n^2)\to O(n),\quad \text{计算量不变}
$$

用途：长序列训练/推理。易错：它省显存与搬运，不减 FLOPs，算力受限时不会变快。

### 92. MoE 计算

$$
\text{激活参数}\approx\frac{k}{N}\times\text{总参数}
$$

用途：估 MoE 训练成本与显存。易错：FLOPs 按激活算、显存按总算，混用会得出“万亿模型单卡可跑”。

### 93. MLA 压缩比

$$
\text{压缩比}\approx\frac{2n_hd_h}{d_c+d_r}
$$

用途：长上下文 KV 成为瓶颈时估收益。易错：省的是带宽，花的是每次投影的算力。

### 94. TTFT 与 TPOT

$$
\text{总时延}\approx\mathrm{TTFT}+\mathrm{TPOT}\times\text{输出长度}
$$

用途：定 SLA、拆延迟瓶颈。易错：TTFT 靠算力，TPOT 靠带宽，优化方向相反。

### 95. 量化误差界

$$
\text{单权重误差}\le\frac{\Delta}{2},\quad \Delta=\frac{\max-\min}{2^b-1}
$$

用途：判断位宽够不够。易错：单权重误差小不代表累加后小，误差约随 $\sqrt{\text{维度}}$ 放大。

### 96. Little 定律

$$
\text{并发数}=\text{吞吐}\times\text{平均时延}
$$

用途：容量规划。易错：批处理提吞吐但抬延迟，不能同时最优。

### 97. 专家容量因子

$$
\text{每专家槽位}=\frac{\text{tokens}\times top_k}{\text{专家数}}\times\text{容量因子}
$$

用途：训练 MoE 调容量。易错：因子太小丢信号，太大费显存；常用 1.25。

### 98. 量化后显存

$$
\text{显存}\approx N\times\frac{b}{8}\ \text{字节}
$$

用途：部署前算能不能塞进卡。易错：4bit 实际还要加缩放因子、异常值通道与未量化部分。

### 99. 批大小与显存

$$
\text{KV 增量}=\text{每 token KV}\times\text{序列长度}\times\text{batch}
$$

用途：调并发上限。易错：权重固定，KV 随 batch 与长度线性涨，长上下文时是主导项。

### 100. 缓存命中的节省

$$
\text{实际成本}=\text{未命中全价}+\text{命中部分}\times\text{折扣}
$$

用途：多轮对话、固定系统提示的收益估算。易错：只算单价不算命中率，命中率低时缓存不省。

### 101. 量化的吞吐上限

$$
\text{吞吐}\le\frac{\text{显存带宽}}{\text{参数量}\times b/8}
$$

用途：判断量化后能快多少。易错：这是理论上限，实测常打七到八折。

### 102. 投机解码的最优草稿长度

$$
\gamma_{\text{opt}}\approx\sqrt{\frac{2}{c(1-\alpha)}}\ \text{的量化近似}
$$

用途：调草稿长度。易错：固定 $\gamma$ 不调，接受率一变最优值就变。

### 103. KV cache 的读放大

$$
\text{每步读 KV}=2\times L\times\text{seq}\times n_{kv}\times d_{\text{head}}\times\text{bytes}
$$

用途：解释长上下文为什么慢。易错：只盯权重体积，长上下文时读 KV 的带宽常超过读权重。

### 104. 稀疏注意力的成本

$$
\text{成本}\propto n\times k
$$

用途：设计长上下文时估成本。易错：只看 FLOPs 不看访存，很多稀疏模式实测加速远小于理论。

## 常见误解

- “扩散训练 1000 步，采样也要 1000 步。”采样常 20–50 步，流匹配可到个位数。
- “CFG 免费提升质量。”它一直是双倍前向。
- “4bit 显存就是除以 4。”还有缩放因子与异常值开销。

## 自测

1. 70B、int4 权重显存约多少？还能开 128K 吗？
2. LoRA $r=16$、$d=k=4096$，可训参数约多少？
3. 单请求 10 秒、要撑 100 并发，需要多少吞吐？

## 复习锚点

- 生成看步数与引导，效率看位宽与带宽，服务看延迟与并发。
- 先确认瓶颈，再选优化。
- 公式给上限，实测打折扣。

## 来源

<https://mp.weixin.qq.com/s/5J2KoDfP7FFfS6ojHmxuAw>
