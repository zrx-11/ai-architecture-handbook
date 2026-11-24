# 第 7 章：架构公式（1–20）

这一组公式只回答“模型有多大、注意力多贵、一张图/一段视频占多少 token”。先记单位，再记系数。

## 一句话核心

架构公式的用途是估量级，不是精确复现论文数字；每个结果后面都要跟一句“这是单层、单头、单请求还是整个模型”。

## 学习目标

- 能手算一层注意力的参数量、KV cache 和图像 token 数。
- 能解释 GQA 为什么只省显存、不省 FLOPs。
- 能判断一个“参数量很大”的说法是总参数还是激活参数。

## 公式清单

### 1. 注意力

$$
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

用途：序列建模的默认起点；只有超长、算力极紧或流式内存恒定时才换线性/稀疏方案。易错：$O(n^2d)$ 只是注意力本身，整模型还有 FFN 的 $O(nd^2)$。

### 2. 多头注意力

$$
\operatorname{head}_i=\operatorname{Attention}(QW_i^Q,KW_i^K,VW_i^V),\quad
\operatorname{MultiHead}=\operatorname{Concat}(\operatorname{head}_1,\ldots,\operatorname{head}_h)W^O
$$

用途：把 $d$ 维切成 $h$ 份并行学不同关系。易错：头不是越多越好，单头维度低于 64 左右，表达力会退化。

### 3. softmax

$$
\operatorname{softmax}(z_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
$$

用途：注意力权重、分类头、MoE 路由。易错：logits 差 10 已经接近 1:22000，差 20 基本为 0。

### 4. RoPE

$$
\theta_i=\frac{m}{10000^{2i/d}},\quad
[x,y]\mapsto[x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta]
$$

用途：把位置写成旋转角，让注意力依赖相对位移。易错：超过训练长度仍会退化，要配 YaRN/NTK。

### 5. RMSNorm

$$
\operatorname{RMSNorm}(x)=\gamma\cdot\frac{x}{\sqrt{\operatorname{mean}(x^2)+\varepsilon}}
$$

用途：新模型默认归一化，比 LayerNorm 少一次减均值。易错：$\varepsilon$ 不能省，均方根接近 0 会放大噪声。

### 6. 残差与层归一化

$$
x'=\operatorname{LayerNorm}(x+F(x)),\quad
\operatorname{LN}(x)=\gamma\frac{x-\mu}{\sqrt{\sigma^2+\varepsilon}}+\beta
$$

用途：让深层网络尺度不漂移。易错：深模型通常用 pre-LN，残差分支还要乘 $1/\sqrt{2N}$。

### 7. 前馈网络

$$
\operatorname{FFN}(x)=W_2\cdot\operatorname{act}(W_1x)
$$

用途：逐 token 升维再降维，是 block 参数大头。易错：GELU 时代是 4 倍，SwiGLU 约 8/3 倍，照 4 倍会高估。

### 8. 状态空间递推

$$
h_t=Ah_{t-1}+Bx_t,\quad y_t=Ch_t
$$

用途：固定状态随序列滚动，推理内存恒定。易错：$A$ 的特征值必须在单位圆内，否则状态发散。

### 9. 图像 token 数

$$
\text{tokens}=\frac{H}{P}\times\frac{W}{P}
$$

用途：多模态成本第一道闸门。易错：分辨率翻倍是 4 倍 token，不是 2 倍；1024²、patch 14 约 5,400 token。

### 10. QKV 参数量

$$
\text{每层注意力参数}\approx 4d^2
$$

用途：估模型规模、判断要不要 GQA/MLA。易错：FFN 往往更大，SwiGLU 约 $8d^2$，别只盯注意力。

### 11. 感受野随层数

$$
\text{理论感受野}\approx \text{层数}\times\text{局部窗口}
$$

用途：估滑窗模型能覆盖多远。易错：理论感受野不等于有效感受野，注意力权重沿距离衰减。

### 12. GQA 的 KV 缩减

$$
\text{缩减比}=\frac{n_{kv}}{n_h}
$$

用途：估 GQA 省多少 KV。易错：只缩 KV cache，不缩注意力 FLOPs。

### 13. 注意力掩码显存

$$
\text{掩码大小}=n^2\times \text{batch}\times \text{字节数}
$$

用途：长上下文训练显存估算。易错：FlashAttention 类实现可以不物化这块，不要重复计入。

### 14. 视频 token 数

$$
\text{tokens}=\frac{T}{p_t}\times\frac{H}{P}\times\frac{W}{P}
$$

用途：估视频生成/理解成本。易错：分辨率和时长各翻倍，token 是 8 倍，不是 2 倍。

### 15. 位置编码波长

$$
\lambda_i=2\pi\cdot10000^{2i/d}
$$

用途：判断最长波长能否覆盖目标上下文。易错：波长够长也不等于能外推，超过训练分布仍会退化。

### 16. 归一化层参数占比

$$
\text{占比}\approx\frac{4d}{12d^2}=\frac{1}{3d}
$$

用途：判断参数优化优先级。易错：它的成本在归约计算，不在参数；$d=4096$ 时约 0.008%。

### 17. 嵌入参数与词表

$$
\text{嵌入参数}=V\times d
$$

用途：估词表带来的参数。易错：多语言模型词表常扩到 12.8 万以上，嵌入会明显变大。

### 18. 每头维度

$$
d_{\text{head}}=\frac{d}{h}
$$

用途：设计头数，先定 $d_{\text{head}}\ge64$ 再反推。易错：一味加头把每头压到 64 以下，注意力会退化成平均。

### 19. FFN 参数占比

$$
\text{占比}\approx\frac{8d^2}{4d^2+8d^2}=\frac{2}{3}
$$

用途：解释为什么 MoE 要替换 FFN。易错：这是 SwiGLU 口径；不同激活与中间维度会变。

### 20. 多模态 token 预算

$$
\text{总长}=\text{文本 token}+\text{图像 token}\times\text{图数}
$$

用途：多图与长文档混合输入前先算总长。易错：按文本长度估上下文，多图请求的真实占用常是文本十倍。

## 常见误解

- 公式算出的是“单层/单请求”的量，不是整个模型。
- 参数量与计算量要分开：总参数看显存，激活参数看 FLOPs。
- 视觉 token 与文本 token 共享同一个上下文窗口，不是免费的。

## 自测

1. 8K 序列、单头 $d=128$、fp16，注意力分数矩阵约多大？
2. $d=4096$、$h=32$ 时每头多少维？$h=64$ 呢？
3. 70B、bf16 的权重显存约多少？KV 另算多少？

## 复习锚点

- 先单位，后系数。
- 单层、单头、单请求、整模型，四个口径别混。
- 省显存不等于省算力。

## 来源

<https://mp.weixin.qq.com/s/5J2KoDfP7FFfS6ojHmxuAw>
