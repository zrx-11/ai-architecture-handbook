# 第 8 章：训练公式（21–43）

这一组回答“损失怎么算、优化器怎么走、显存和步数怎么估”。不要背所有系数，先记 6ND、16 字节/参数、有效 batch 这三个。

## 一句话核心

训练公式的每个结果都要乘一个现实系数：MFU、通信效率、数据利用率。公式给下界，实测给结论。

## 学习目标

- 能手算交叉熵、困惑度、一次 Adam 更新。
- 能估训练显存、训练步数、检查点大小。
- 能解释梯度累积、梯度裁剪、预热与 batch 缩放的关系。

## 公式清单

### 21. 交叉熵

$$
L=-\sum_i y_i\log p_i
$$

用途：分类与语言建模的默认损失。易错：标签平滑会改变最优解，正确类不再需要趋近 1。

### 22. 困惑度

$$
\operatorname{PPL}=e^{L}
$$

用途：同分布预训练损失对比。易错：跨数据集、跨分词器不可比，不能拿来对外宣传。

### 23. 均方误差

$$
L=\frac1n\sum_i(y_i-\hat y_i)^2
$$

用途：回归默认损失。易错：对离群点极敏感，10 倍误差贡献是 100 倍。

### 24. 链式法则

$$
\frac{\partial L}{\partial x}=\frac{\partial L}{\partial y}\cdot\frac{\partial y}{\partial x}
$$

用途：反向传播的局部计算。易错：一次反向约前向两倍计算量，但要多存激活。

### 25. SGD 与动量

$$
\theta\leftarrow\theta-\eta g,\quad
v\leftarrow\beta v+g,\quad
\theta\leftarrow\theta-\eta v
$$

用途：小模型、教学、窄损失面。易错：学习率与动量耦合，改一个要重调另一个。

### 26. Adam

$$
m\leftarrow\beta_1m+(1-\beta_1)g,\quad
v\leftarrow\beta_2v+(1-\beta_2)g^2
$$
$$
\theta\leftarrow\theta-\eta\frac{\hat m}{\sqrt{\hat v}+\varepsilon}
$$

用途：绝大多数训练的默认优化器。易错：7B 模型 Adam 状态约 56 GB；大模型 $\varepsilon$ 常要放大。

### 27. 学习率调度

$$
lr_t=lr_{\min}+\frac12(lr_{\max}-lr_{\min})\left(1+\cos\frac{\pi t}{T}\right)
$$

用途：长训练预热 + 余弦退火。易错：步数按优化器更新次数算，不是 micro-batch 次数。

### 28. 批次与学习率

$$
lr=lr_{\text{base}}\times\frac{\text{batch}}{\text{batch}_{\text{base}}}
$$

用途：扩 batch 时调学习率。易错：跨过临界 batch 后收益消失，继续线性放大可能发散。

### 29. 梯度累积

$$
\text{等效 batch}=\text{micro-batch}\times\text{accum\_steps}\times\text{DP}
$$

用途：显存不够时凑大 batch。易错：学习率调度要按等效步数算；BatchNorm 一类跨样本统计不适用。

### 30. 梯度裁剪

$$
g\leftarrow g\cdot\min\left(1,\frac{c}{\|g\|}\right)
$$

用途：防单步爆炸。易错：裁得太狠，模型只学“安全的步”，收敛变慢。

### 31. MoE 负载均衡损失

$$
L_{\text{aux}}=\alpha N\sum_i f_iP_i
$$

用途：惩罚负载集中，防专家塌缩。易错：$\alpha$ 太大会压过主损失；专家上百后本身难调。

### 32. μP 缩放

$$
lr\propto\frac1{\text{width}},\quad \text{初始化方差}\propto\frac1{\text{width}}
$$

用途：跨宽度迁移超参。易错：只对宽度成立，加层数仍要重调。

### 33. MTP 损失

$$
L=\sum_{k=1}^{K}-\log P(x_{t+k}\mid x_{\le t})
$$

用途：训练时让模型往后看几步，头可当投机解码草稿。易错：$K$ 太大收益饱和，常取 2–4。

### 34. 检查点大小

$$
\text{字节/参数}\approx2+2+4+4+4=16
$$

用途：估存储与加载时间。易错：只按 2 字节/参数估会低估 8 倍。

### 35. 序列打包利用率

$$
\text{利用率}=\frac{\text{平均长度}}{\text{最大长度}}
$$

用途：短样本多的数据集用 packing 提利用率。易错：必须配正确注意力掩码，否则样本互相看见。

### 36. 数据重复与收益递减

$$
\text{有效数据}\approx\text{唯一 token}+\text{重复部分折价}
$$

用途：高质量语料不足时估重复价值。易错：4 轮以内近似无损，之后收益快速衰减；大模型更容易记住重复。

### 37. EMA 权重

$$
\theta_{\text{ema}}\leftarrow decay\cdot\theta_{\text{ema}}+(1-decay)\theta
$$

用途：评测/部署用滑动平均，通常比最后一步稳。易错：训练初期 EMA 滞后明显，步数少时意义不大。

### 38. 梯度噪声尺度

$$
B_{\text{noise}}\approx\frac{\operatorname{tr}(\Sigma)}{\|g\|^2}
$$

用途：判断再加卡还有没有用。易错：它随任务、模型、阶段变化，不能跨实验直接套。

### 39. 训练总步数

$$
\text{steps}=\frac{D}{\text{batch}\times\text{seq}}
$$

用途：配学习率调度、日志与检查点周期。易错：用 micro-batch 算会把步数高估几十倍。

### 40. 检查点重算代价

$$
\text{期望重算步数}=\frac{\text{间隔}}{2}
$$

用途：决定检查点间隔。易错：只算重算时间，漏掉百 GB 检查点的加载时间。

### 41. 每卡权重体积

$$
\text{每卡权重}=\frac{\text{总参数}\times\text{字节数}}{\text{并行度}}
$$

用途：判断能不能纯数据并行。易错：DP 每卡一份完整权重，只有 TP/PP 才切片。

### 42. 预热按 token 计

$$
\text{warmup\_tokens}=\text{warmup\_steps}\times\text{batch}\times\text{seq}
$$

用途：换 batch/seq 时保持预热样本量一致。易错：只记步数，batch 一改预热 token 量就变。

### 43. 数据并行的梯度压缩

$$
\text{压缩比}=\frac{\text{原始梯度体积}}{\text{压缩后体积}}
$$

用途：带宽受限时减少同步量。易错：压缩率越高收敛越慢，省下的通信可能被多走的步数抵消。

## 一张纸训练账本

1. 参数显存：$N\times$ 字节/参数。
2. 激活显存：随 batch、seq、层数线性涨。
3. 训练 FLOPs：$6ND$。
4. 通信量：DP 约 $2N$，TP/EP 看层内与 all-to-all。
5. 时间：FLOPs /（卡数 × 单卡算力 × MFU）。

## 常见误解

- “6ND 是精确值。”它漏了注意力二次项，长序列会偏小。
- “梯度累积等于大 batch。”BatchNorm 一类跨样本统计会失真，学习率调度也要按等效步数算。
- “检查点只存权重。”优化器状态、数据位置、随机数状态都要存。

## 自测

1. 7B 模型 bf16 训练，按 16 字节/参数估显存多少？
2. 2T token、batch 512、seq 8K，总步数约多少？
3. 为什么 DP 加卡不能装下更大模型？

## 复习锚点

- 16 字节/参数、6ND、有效 batch。
- 公式给下界，MFU 与通信效率给现实。
- 先算显存，再算算力，最后算时间。

## 来源

<https://mp.weixin.qq.com/s/5J2KoDfP7FFfS6ojHmxuAw>
