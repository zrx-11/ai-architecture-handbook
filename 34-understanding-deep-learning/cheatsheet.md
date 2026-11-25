# 速查：UDL 核心式子

## 基础

- 线性回归：\(\hat y=w^\top x+b\)
- 单隐层：\(f(x)=w_2^\top\mathrm{ReLU}(W_1x+b_1)+b_2\)
- 梯度下降：\(\theta_{t+1}=\theta_t-\eta\nabla L(\theta_t)\)

## 架构

- 卷积：\(Y_{i,j}=\sum_{m,n}X_{i+m,j+n}K_{m,n}+b\)
- 残差：\(y=x+F(x)\)
- 注意力：\(\mathrm{softmax}(QK^\top/\sqrt{d_k})V\)
- GCN：\(H'=\sigma(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}HW)\)

## 生成

- 变量替换：\(p_X(x)=p_Z(f^{-1}(x))|\det J|\)
- ELBO：\(\mathbb{E}_q[\log p(x|z)]-\mathrm{KL}(q(z|x)\|p(z))\)
- 扩散目标：\(\mathbb{E}\|\epsilon-\epsilon_\theta(x_t,t)\|^2\)

## 决策

- 回报：\(G_t=\sum_k\gamma^kR_{t+k+1}\)
- 贝尔曼最优：\(Q^*(s,a)=R+\gamma\mathbb{E}[\max_{a'}Q^*(s',a')]\)
