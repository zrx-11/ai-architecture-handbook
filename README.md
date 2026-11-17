# AI 架构学习系统：从机器学习到 DeepSeek

**在线访问**：<https://zrx-11.github.io/deepseek-architecture-learning/>  
**仓库**：<https://github.com/zrx-11/deepseek-architecture-learning>

给数学和代码接近零基础的学习者，把“数学 → Python → 经典机器学习 → 神经网络 → 深度学习 → Transformer / SVM → 强化学习 → DeepSeek R1/V4/V4.1 → 多模态 → 评测 → 部署”连成一条可以按依赖顺序走的学习路径。不是只讲 Transformer，也不是只有论文摘要。

## 界面

默认深色，DeepSeek 钴蓝 + 鲸青，衬线标题配点阵底纹。首页右侧是“总参数 / 每 token 激活”参数栈，七步主线是一条连续 rail；正文页有面包屑、出处徽标和可横向滚动的宽表。手机端目录是抽屉，390px 下页面不横向溢出。浅色主题是暖灰纸感，不是纯白。

视觉方向与改动清单见 [`视觉重构说明.md`](视觉重构说明.md)。

## 先说明一个事实

DeepSeek 更准确的说法是**开放权重**，不是“全部开源”：模型权重、技术报告、部分推理与训练框架代码公开；完整训练数据、数据清洗流程和端到端训练流水线没有公开。架构层面（`modeling_deepseek.py`、`configuration_deepseek.py` 里的 MLA、DeepSeekMoE、MTP 等结构）是公开且可复现的，但“架构开源”不等于“整个模型全流程开源”。

V4 / V4.1 的论文口径以公开技术报告为准；报告没有展开的 kernel 级细节、`num_hash_layers` 等，正文标“待确认”，不把二手解读补成事实。

## 这套材料有什么

### 7 本分册

| 分册 | 内容 | 规模 |
|---|---|---|
| 基础篇：从零到 Transformer | 向量、矩阵、softmax、参数与梯度、注意力、Transformer 一层楼、V3 的 MLA/MoE/MTP、形状与手算附录 | 6 章 / 16 概念 / 15 测验 / 20 卡片 / 23 术语 |
| 论文拆解：R1 / V4 / V4.1 | 按“问题—方法—数据—实验—局限”逐篇拆三篇报告，附公式逐项拆解 | 5 章 / 15 概念 / 12 测验 / 16 卡片 / 26 术语 |
| 架构阐释：三代模型的设计逻辑 | 瓶颈迁移、组件演进、训练路线、选型与取舍，附 1M 上下文选型算例 | 5 章 / 5 概念 / 12 测验 / 16 卡片 / 20 术语 |
| 机器学习基础：从任务到评估 | 周志华《机器学习》导读：评估、线性模型、决策树、神经网络、SVM、贝叶斯、集成、聚类、降维、半监督、概率图、强化学习 | 16 章 / 2 概念 / 47 测验 / 68 卡片 / 72 术语 |
| 神经网络：从一条直线推到反向传播 | 函数、导数、链式法则、点积、神经元、激活、前向、损失、梯度下降、反向传播、过拟合 | 13 章 / 12 概念 / 32 测验 / 34 卡片 / 55 术语 |
| 深度学习入门：从零手写神经网络 | Python、感知机、两层网络、反向传播、正则化、CNN | 8 章 / 2 概念 / 21 测验 / 38 卡片 / 38 术语 |
| DeepSeek 模型全谱 | dense → DeepSeekMoE → V2/MLA → V3/MTP → R1/GRPO → V3.1/V3.2/DSA → V4/CSA/HCA/mHC/Muon → V4.1/CED/CSA2/Engram/DSpark，以及 VL/VL2、Janus、OCR/OCR2、Prover-V2、Math-V2 | 14 章 / 13 概念 / 42 测验 / 44 卡片 / 68 术语 |

### 15 套深潜课（164 节）

| 类别 | 课程 | 节数 | 解决的问题 |
|---|---|---|---|
| 数学与代码 | 数学基础 | 12 | 函数、向量、矩阵、导数、链式法则、概率、softmax、交叉熵 |
| 数学与代码 | Python 与 NumPy | 10 | 变量、函数、shape、广播、矩阵乘、手写梯度下降 |
| 经典 ML | 经典机器学习 | 12 | 回归、树、聚类、PCA、偏差方差、交叉验证、数据泄漏 |
| 经典 ML | CNN 与 RNN | 10 | 卷积、池化、感受野、残差、LSTM/GRU、seq2seq |
| 神经网络 | 反向传播与优化器 | 10 | 计算图、2-2-1 手算、梯度消失、SGD/Momentum/Adam |
| Transformer | Transformer 深潜 | 15 | 从初中数学推到一层 Transformer、训练与生成 |
| 经典 ML | SVM 深潜 | 16 | 最大间隔、对偶、KKT、软间隔、核技巧 |
| DeepSeek | MoE 与 MLA | 10 | 路由、共享专家、KV cache、MLA、MTP、DSA |
| DeepSeek | DeepSeek 架构深潜 | 13 | MoE/MLA/MTP/DSA/CSA/HCA/mHC/Muon/Engram/DSpark/V4.1 |
| 强化学习 | 强化学习与 GRPO | 10 | MDP、策略梯度、PPO、奖励模型、组内优势、KL/熵 |
| 系统 | 训练与推理账本 | 9 | 6ND、KV 公式、prefill/decode、DP/TP/PP/EP、量化 |
| 评测 | 概率、损失与评估 | 10 | 贝叶斯、交叉熵、P/R/F1、AUC、数据泄漏 |
| 多模态 | 多模态模型 | 9 | ViT、CLIP、VL 三段式、Janus、OCR/OCR2、Prover/Math-V2 |
| 安全 | 评测与安全 | 9 | pass@k、LLM 裁判偏差、幻觉、对齐/拒答、红队、数据污染 |
| 部署 | 推理部署 | 9 | KV cache、PagedAttention、continuous batching、并行、SLA |

合计 **67 个分册章节、65 个概念页、181 道测验、236 张抽认卡、302 条分册术语、15 套 164 节深潜课**。另有跨书术语总表、学习节点地图、跨书概念映射、深潜专题、知识覆盖地图和综合检验。

## 七步主线

首页只给一条主线，不按顺序堆料：

1. **数学与 Python 工具**：数学基础 + Python/NumPy。
2. **机器学习与神经网络**：经典 ML + 机器学习分册 + 神经网络分册。
3. **Transformer 与序列模型**：基础篇 + CNN/RNN + Transformer 深潜。
4. **读三篇论文**：R1、V4、V4.1 按固定五问拆。
5. **三代架构与全家族**：架构阐释 + 架构深潜 + 模型全谱 + 多模态。
6. **训练、强化学习与账本**：强化学习/GRPO + 训练推理账本 + 概率评估。
7. **评测、安全与上线**：评测与安全 + 推理部署 + 选型表。

每一步先读主入口，卡住再从资料库补；资料库默认折叠，避免首页一次铺 22 个入口。

## 怎么用

1. 双击根目录 `index.html`，先按七步主线走。每步只读一个主入口，不要一次开很多。
2. 每章先看“一句话核心”和“学习目标”，再读讲解，最后做自测；低于 80% 就回到对应概念页。
3. 侧边栏“诊断”随机抽 5 题；答错会沿 `prerequisites` 依赖链倒推根因。
4. 高难概念页底部的“展开完整第一性原理推导”默认折叠，点开看逐步代数过程与数值算例。
5. 深潜课在根目录的 `07-…` 到 `22-…` 子目录，自包含 HTML，保留交互、公式与折叠推导。
6. 进度保存在浏览器本地，可导出/导入 JSON；各书进度独立，深潜课进度单独保存。

## 目录结构

```
index.html                 总学习手册（单文件入口）
index.md                   Markdown 导航
00-跨书总览/               推荐顺序、概念映射、术语总表、节点地图、深潜专题、知识覆盖地图、综合检验
01-foundations/            数学与 Transformer 骨架
02-paper-teardown/         R1 / V4 / V4.1 论文拆解
03-architecture/           三代架构阐释
04-machine-learning/       机器学习基础（周志华导读）
05-neural-networks/        神经网络从零
06-deep-learning/          深度学习入门（代码线）
07-transformer-deep/       Transformer 从零推导（深潜，自包含）
08-svm-deep/               SVM 从零推导（深潜，自包含）
09-deepseek-family/        DeepSeek 全家族：14 章 + 模型卡索引
10-backprop-deep/          反向传播与优化器（深潜，自包含）
11-moe-mla-deep/           MoE 与 MLA（深潜，自包含）
12-probability-eval-deep/  概率、损失与评估（深潜，自包含）
13-train-infer-deep/       训练与推理账本（深潜，自包含）
14-math-deep/              数学基础（深潜，自包含）
15-python-deep/            Python 与 NumPy（深潜，自包含）
16-classical-ml-deep/      经典机器学习（深潜，自包含）
17-cnn-rnn-deep/           CNN 与 RNN（深潜，自包含）
18-rl-grpo-deep/           强化学习与 GRPO（深潜，自包含）
19-deepseek-arch-deep/     DeepSeek 架构深潜（深潜，自包含）
20-multimodal-deep/        多模态模型（深潜，自包含）
21-eval-safety-deep/       评测与安全（深潜，自包含）
22-serving-deep/           推理部署（深潜，自包含）
_build/                    合并、生成、CDN 修补、验证脚本
_work/                     论文 PDF 与过程数据（不推送公开仓库）
_merge_sources/            合并前的原仓库副本（只留在本地交付包，不推送公开仓库）
```

公开仓库只放站点、章节源码、manifest 与 `_build` 脚本；`_work/`、`_merge_sources/` 与 zip 由 `.gitignore` 排除，避免把论文 PDF 和第三方仓库副本一起推上去。

## 部署到 GitHub Pages

站点是纯静态文件，没有构建步骤。仓库根目录设为本目录内容，然后：

```bash
git add -A
git commit -m "AI 架构学习系统：15 套深潜课 + 知识覆盖地图"
git push origin main
```

仓库 Settings → Pages → Source 选 `Deploy from a branch`，Branch 选 `main`，目录选 `/ (root)`，保存后等 1–2 分钟。

新仓库首次推送：

```bash
git init
git add -A
git commit -m "AI 架构学习系统"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

## 验证结论

- `_build/verify_deep_courses.py`：**144/144 通过**。覆盖 15 套深潜课的标题、节数、目录、公式渲染、5 道测验的正确/错误反馈、下一节切换、390px 无横向滚动、控制台零错误。
- `_build/verify_all.py`：**60/60 通过**。覆盖 7 本书首末章、测验、抽认卡、术语、搜索、移动端/桌面端布局、09 独立伴侣 42 题综合测验、KaTeX/Mermaid、控制台错误。
- 知枢自带 `verify_handbook.py`：67/68 通过；唯一未过项是“同义召回”启发式断言在精确命中时误判，不是页面功能失败。
- 打包后需解压到独立目录冒烟：首页、15 套深潜课各一节、测验、390px/1440px 布局。

## 已知边界

- **视频与音频模型**：只到图像/文档多模态，不展开视频时序、音频编码、语音合成。
- **Agent 与工具学习**：只在安全章节提到工具滥用，不系统讲规划、记忆、多智能体。
- **可解释性**：不展开注意力可视化、探针、电路分析。
- **分布式训练 kernel 级实现**：讲 TP/PP/EP 的账，不讲具体通信库和 kernel 代码。
- **V4/V4.1 未公开细节**：论文没展开的部分标“待确认”，课程不编造。

## 拆分合并来源

| 来源仓库 | 合并到 | 处理方式 |
|---|---|---|
| `zrx-11/SVM` | `08-svm-deep/` | 原样保留单文件 HTML，补 README 与入口 |
| `zrx-11/transformer` | `07-transformer-deep/` | 原样保留单文件 HTML，补 README 与入口 |
| `zrx-11/neural-net-zero` | `05-neural-networks/` | 保留章节/概念/测验/卡片/术语，重建学习伴侣 |
| `zrx-11/ai-ml-dl-rl-enlighten` 的 `02-机器学习` | `04-machine-learning/` | 拆成独立分册，改 slug/标题，重建学习伴侣 |
| `zrx-11/ai-ml-dl-rl-enlighten` 的 `03-深度学习入门` | `06-deep-learning/` | 拆成独立分册，改 slug/标题，重建学习伴侣 |

原仓库没有被修改、移动或删除；本仓库是合并后的学习站点。
