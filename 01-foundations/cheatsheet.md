# 速查表

## 公式与规则
| 场景 | 内容 |
|---|---|
| 矩阵乘向量 | 每行与向量做点积 |
| softmax | $e^{z_i}/\sum_j e^{z_j}$ |
| 梯度下降 | $w\leftarrow w-\eta\partial L/\partial w$ |
| 注意力分数 | $q\cdot k/\sqrt{d_k}$ |
| 注意力输出 | $\sum_j\alpha_{ij}v_j$ |
| 残差 | $y=x+\mathrm{Layer}(x)$ |
| RMSNorm | $x/\sqrt{\mathrm{mean}(x^2)+\epsilon}\odot g$ |

## 关键数字
| 项目 | 数值 |
|---|---|
| V3 总参数 / 激活 | 671B / 37B |
| V3 层数 / 头数 | 61 / 128 |
| V3 路由专家 / 激活 | 256 / 8 |
| V3 预训练 token | 14.8T |
| V3 上下文 | 128K |
