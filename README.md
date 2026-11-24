# AI 架构学习手册：从数学与编程基础到主流大模型架构

**在线访问**：<https://zrx-11.github.io/ai-architecture-handbook/>  
**仓库**：<https://github.com/zrx-11/ai-architecture-handbook>

给数学和代码接近零基础的学习者，把“数学 → Python → 经典机器学习 → 神经网络 → 深度学习 → Transformer → 论文阅读 → DeepSeek 三代案例 → 全球开放模型 → 多模态 → 评测 → 部署”连成一条可以按依赖顺序走的学习路径。DeepSeek 是第一个完整案例，不是课程终点；这套材料的主干是主流大模型架构分析。

## 界面

默认深色，DeepSeek 钴蓝 + 鲸青，衬线标题配点阵底纹。首页右侧是“总参数 / 每 token 激活”参数栈，八步主线是一条连续 rail；正文页有面包屑、出处徽标和可横向滚动的宽表。手机端目录是抽屉，390px 下页面不横向溢出。浅色主题是暖灰纸感，不是纯白。

视觉方向与改动清单见 [`视觉重构说明.md`](视觉重构说明.md)。

## DeepSeek 在本课程里的位置

DeepSeek 是主线上的“完整案例”，用来练三件事：读论文、拆架构、算账。它不是唯一内容，后面还有全球开放模型对照。DeepSeek 更准确的说法是**开放权重**，不是“全部开源”：权重、技术报告、部分推理与训练框架代码公开；完整训练数据、数据清洗流程和端到端训练流水线没有公开。

V4 / V4.1 的论文口径以公开技术报告为准；报告没有展开的 kernel 级细节、`num_hash_layers` 等，正文标“待确认”，不把二手解读补成事实。

## 这套材料有什么

### 14 本分册

| 分册 | 内容 | 规模 |
|---|---|---|
| 基础篇：从数字到 Transformer | 向量、矩阵、softmax、参数与梯度、注意力、Transformer 一层楼、V3 的 MLA/MoE/MTP、形状与手算附录 | 6 章 / 16 概念 / 15 测验 / 20 卡片 / 23 术语 |
| 案例论文拆解：DeepSeek R1 / V4 / V4.1 | 按“问题—方法—数据—实验—局限”逐篇拆三篇报告，附公式逐项拆解 | 5 章 / 15 概念 / 12 测验 / 16 卡片 / 26 术语 |
| 案例架构：DeepSeek 三代设计逻辑 | 瓶颈迁移、组件演进、训练路线、选型与取舍，附 1M 上下文选型算例 | 5 章 / 5 概念 / 12 测验 / 16 卡片 / 20 术语 |
| 机器学习基础：从任务到评估 | 周志华《机器学习》导读：评估、线性模型、决策树、神经网络、SVM、贝叶斯、集成、聚类、降维、半监督、概率图、强化学习 | 16 章 / 2 概念 / 47 测验 / 68 卡片 / 72 术语 |
| 神经网络：从一条直线推到反向传播 | 函数、导数、链式法则、点积、神经元、激活、前向、损失、梯度下降、反向传播、过拟合 | 13 章 / 12 概念 / 32 测验 / 34 卡片 / 55 术语 |
| 深度学习入门：从零手写神经网络 | Python、感知机、两层网络、反向传播、正则化、CNN | 8 章 / 2 概念 / 21 测验 / 38 卡片 / 38 术语 |
| 案例全谱：DeepSeek 一代到 V4.1 | dense → DeepSeekMoE → V2/MLA → V3/MTP → R1/GRPO → V3.1/V3.2/DSA → V4/CSA/HCA/mHC/Muon → V4.1/CED/CSA2/Engram/DSpark，以及 VL/VL2、Janus、OCR/OCR2、Prover-V2、Math-V2 | 14 章 / 13 概念 / 42 测验 / 44 卡片 / 68 术语 |
| 全球开放模型全谱 | Llama / Qwen / Mistral / Gemma / Phi / Falcon / OLMo / GLM / Kimi / MiniMax / InternLM / MiniCPM / Step / ERNIE / Ling / MiMo，以及 MoE、非 Transformer、多模态、许可证、config 与 101 行模型索引 | 16 章 / 12 概念 / 53 测验 / 48 卡片 / 70 术语 |
| AI 机制与公式总库 | 114 个机制 + 104 个公式，覆盖架构、训练、对齐、推理、生成、应用与安全；每条给“是什么、代价、回哪章” | 11 章 / 8 概念 / 23 测验 / 22 卡片 / 25 术语 |
| AI 导论：Hello, AI | 上海交大 AI+ 教材：AI 全景、搜索/规则/强化、神经网络、语言模型、对齐、RAG、多模态、智能体 | 20 章 / 50 概念 / 60 测验 / 70 卡片 / 110 术语 |
| AI 现代方法：完整地图 | AIMA 第 4 版：搜索、逻辑、规划、不确定性、决策、机器学习、深度学习、强化学习与部署 | 28 章 / 2 概念 / 56 测验 / 92 卡片 / 87 术语 |
| 动手学深度学习：原理与代码 | 从张量、自动求导、MLP、CNN、RNN 到注意力；每个模型配可运行代码 | 11 章 / 2 概念 / 29 测验 / 42 卡片 / 39 术语 |
| 强化学习：Sutton & Barto | MDP、贝尔曼方程、动态规划、蒙特卡洛、TD、n 步自举、规划与学习、策略梯度 | 17 章 / 2 概念 / 46 测验 / 64 卡片 / 62 术语 |
| LLM 从零实现：训练、对齐与部署 | BPE、位置编码、注意力、GPT 组装、预训练、SFT、LoRA、DPO/GRPO、KV cache、量化、RAG/Agent、评测与最小可复现路线 | 14 章 / 14 概念 / 28 测验 / 28 卡片 / 56 术语 |


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

合计 **184 个分册章节、155 个概念页、476 道测验、602 张抽认卡、751 条分册术语、15 套 164 节深潜课**。另有 7 个同源资料馆：126 讲机理深研、306 个模型清单、27 章概率统计、24 本数学先修、26 章智能体设计模式、20 门课程地图、500+ 板块 AI 简史；以及跨书术语总表、学习节点地图、跨书概念映射、深潜专题、知识覆盖地图和综合检验。

## 八步主线

首页只给一条主线，不按顺序堆料：

1. **数学与编程工具**：数学基础 + Python/NumPy；先补到能算、能写。
2. **机器学习与神经网络**：经典 ML + 机器学习分册 + 神经网络分册 + 反向传播。
3. **深度学习与序列模型**：深度学习入门 + CNN/RNN + Transformer 基础。
4. **Transformer 与论文阅读**：基础篇 + Transformer 深潜 + 论文拆解；DeepSeek 三篇作为阅读样例。
5. **案例架构：DeepSeek 三代**：架构阐释 + 架构深潜 + 模型全谱 + 多模态；学“瓶颈—机制—代价”的分析方法。
6. **全球开放模型对照**：全球分册 + MoE/MLA + 101 行模型索引；把同一套读法用到 Llama/Qwen/Mistral 等家族。
7. **从零实现一次 LLM**：BPE + tiny GPT + 预训练 + SFT/LoRA + DPO/GRPO + KV/RAG/评测；先用 CPU 或单卡跑通一条可验收链路。
8. **训练、评测与部署**：强化学习/GRPO + 训练推理账本 + 评测安全 + 推理部署；最后做选型。

每一步先读主入口，卡住再从资料库补；资料库默认折叠。第 9 本“AI 机制与公式总库”是回查书；第 10–14 本是 AI 导论、AIMA、动手学深度学习、Sutton 强化学习和 LLM 从零实现，作为广度、教材与实战对照，不强行插进主线。

### 全球对照线（第六步，第八本书）

全球分册作为主线的第 6 步，也可单独走 7 步：边界与地图 → Llama/Qwen → Mistral/Gemma/Phi → 北美/中国其他 → 非 Transformer/MoE → 多模态/注意力 → 许可证/评测/config/索引。它回答的是“Llama 之外还有什么、同一件事别的家族怎么做、拿到一个开放模型怎么读”。

## 怎么用

1. 双击根目录 `index.html`，先按八步主线走。每步只读一个主入口，不要一次开很多。
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
23-global-open-models/     全球开放模型全谱：16 章 + 101 行家族索引
14-llm-from-scratch/       LLM 从零实现：训练、对齐与部署（14 章）
24-ai-mechanisms-formulas/ AI 机制与公式总库：114 机制 + 104 公式（回查书）
25-hello-ai/               AI 导论：Hello, AI（20 章）
26-ai-modern-methods/      AIMA 现代方法：完整地图（28 章）
27-d2l/                    动手学深度学习：原理与代码（11 章）
28-rl-sutton/              Sutton & Barto 强化学习（17 章）
29-ai-study-notes/         AI 机理深研 126 讲（单文件扩展）
30-llm-model-catalog/      全球大模型清单 306 个（单文件扩展）
31-probability-statistics/ 概率统计从零推导 27 章（单文件扩展）
32-math-basics/            数学基础知识丛书 24 本（先修书库）
33-agentic-design-patterns/ 智能体设计模式 26 章（Agent 扩展）
_build/                    合并、生成、CDN 修补、验证脚本
_work/                     论文 PDF 与过程数据（不推送公开仓库）
_merge_sources/            合并前的原仓库副本（只留在本地交付包，不推送公开仓库）
```

公开仓库只放站点、章节源码、manifest 与 `_build` 脚本；`_work/`、`_merge_sources/` 与 zip 由 `.gitignore` 排除，避免把论文 PDF 和第三方仓库副本一起推上去。

## 部署到 GitHub Pages

站点是纯静态文件，没有构建步骤。仓库根目录设为本目录内容，然后：

```bash
git add -A
git commit -m "AI 架构学习手册：全栈课程 + 机制公式总库"
git push origin main
```

仓库 Settings → Pages → Source 选 `Deploy from a branch`，Branch 选 `main`，目录选 `/ (root)`，保存后等 1–2 分钟。

新仓库首次推送：

```bash
git init
git add -A
git commit -m "AI 架构学习手册"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

## 仓库重合清单

对 `zrx-11` 名下 61 个仓库的逐项处置见 `_build/repo-merge-map.md`：7 个来源已并入，3 个单点站已复用，2 个线上入口保留，其余非 AI 主线项目仅登记。

## 验证结论

- `_build/verify_deep_courses.py`：**144/144 通过**。覆盖 15 套深潜课的标题、节数、目录、公式渲染、5 道测验的正确/错误反馈、下一节切换、390px 无横向滚动、控制台零错误。
- `_build/verify_all.py`：**105/105 通过**。覆盖 14 本书首末章、测验、抽认卡、术语、搜索、移动端/桌面端布局、09 独立伴侣 42 题综合测验、机制公式总库 33 处 KaTeX、Mermaid、控制台错误。
- 知枢自带 `verify_handbook.py`：**106/106 通过**。覆盖 14 本书书卡、首末章、测验、抽认卡、术语、搜索、诊断、主题切换、控制台零错误。
- 打包后需解压到独立目录冒烟：首页、15 套深潜课各一节、测验、390px/1440px 布局。

## 已知边界

- **视频与音频模型**：只到图像/文档多模态，不展开视频时序、音频编码、语音合成。
- **Agent 与工具学习**：只在安全章节提到工具滥用，不系统讲规划、记忆、多智能体。
- **可解释性**：不展开注意力可视化、探针、电路分析。
- **分布式训练 kernel 级实现**：讲 TP/PP/EP 的账，不讲具体通信库和 kernel 代码。
- **V4/V4.1 未公开细节**：论文没展开的部分标“待确认”，课程不编造。
- **全球分册的“所有”口径**：家族级、官方公开可下载权重；量化/微调/合并 checkpoint 不逐条讲，附录给 101 行代表索引。

## 拆分合并来源

| 来源仓库 | 合并到 | 处理方式 |
|---|---|---|
| `zrx-11/SVM` | `08-svm-deep/` | 原样保留单文件 HTML，补 README 与入口 |
| `zrx-11/transformer` | `07-transformer-deep/` | 原样保留单文件 HTML，补 README 与入口 |
| `zrx-11/neural-net-zero` | `05-neural-networks/` | 保留章节/概念/测验/卡片/术语，重建学习伴侣 |
| `zrx-11/ai-ml-dl-rl-enlighten` 的 `02-机器学习` | `04-machine-learning/` | 拆成独立分册，改 slug/标题，重建学习伴侣 |
| `zrx-11/ai-ml-dl-rl-enlighten` 的 `03-深度学习入门` | `06-deep-learning/` | 拆成独立分册，改 slug/标题，重建学习伴侣 |

原仓库没有被修改、移动或删除；本仓库是合并后的学习站点。
