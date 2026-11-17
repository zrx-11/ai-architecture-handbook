# AI 架构学习系统：从机器学习到 DeepSeek

**在线访问**：<https://zrx-11.github.io/deepseek-architecture-learning/>  
**仓库**：<https://github.com/zrx-11/deepseek-architecture-learning>

给数学和代码接近零基础的学习者，把“机器学习 → 神经网络 → 深度学习 → Transformer / SVM → DeepSeek R1/V4/V4.1”连成一条可以按依赖顺序走的学习路径。不是只讲 Transformer，也不是只有论文摘要。

## 先说明一个事实

DeepSeek 更准确的说法是**开放权重**，不是“全部开源”：模型权重、技术报告、部分推理与训练框架代码公开；完整训练数据、数据清洗流程和端到端训练流水线没有公开。架构层面（`modeling_deepseek.py`、`configuration_deepseek.py` 里的 MLA、DeepSeekMoE、MTP 等结构）是公开且可复现的，但“架构开源”不等于“整个模型全流程开源”。

## 这套材料有什么

| 分册 | 内容 | 规模 |
|---|---|---|
| 基础篇：从零到 Transformer | 向量、矩阵、softmax、参数与梯度、注意力、Transformer 一层楼、V3 的 MLA/MoE/MTP、形状与手算附录 | 6 章 / 16 概念 / 3 个深度推导 |
| 机器学习基础：从任务到评估 | 周志华《机器学习》导读：评估、线性模型、决策树、神经网络、SVM、贝叶斯、集成、聚类、降维、半监督、概率图、强化学习 | 16 章 / 47 测验 / 72 术语 |
| 神经网络：从一条直线推到反向传播 | 函数、导数、链式法则、点积、神经元、激活、前向、损失、梯度下降、反向传播、过拟合 | 13 章 / 12 概念 / 32 测验 / 2 个深度推导 |
| 深度学习入门：从零手写神经网络 | Python、感知机、两层网络、反向传播、正则化、CNN | 8 章 / 21 测验 / 38 术语 |
| Transformer 从零推导（深潜） | 初中数学 → 词嵌入 → 位置编码 → 注意力 → 多头 → 残差/归一化 → 前馈 → 编码器 → 解码器/掩码 → 训练/生成 → BERT/GPT → 代码 | 15 节 / 179 个推导步骤 |
| SVM 从零推导（深潜） | 最大间隔 → 硬间隔/对偶/KKT → 手算 → 软间隔/hinge → 核技巧 → 核函数 → 代码实验 → 统计学习理论 | 16 节 |
| 论文拆解：R1 / V4 / V4.1 | 按“问题—方法—数据—实验—局限”逐篇拆三篇报告，附公式逐项拆解 | 5 章 / 15 概念 / 5 个深度推导 |
| 架构阐释：三代模型的设计逻辑 | 瓶颈迁移、组件演进、训练路线、选型与取舍，附 1M 上下文选型算例 | 5 章 / 5 概念 |
| DeepSeek 模型全谱 | dense → MoE → MLA → DSA/CSA → V4.1，全家族 105+ 张模型卡索引，附手算与源码地图 | 14 章 / 13 概念 / 42 测验 / 68 术语 |

合计 67 个分册章节、65 个概念页、181 道测验、236 张抽认卡、302 条分册术语，外加两套 31 节的深潜课。另有跨书术语总表、学习节点地图、跨书概念映射和综合检验。

## 三条学习路线

**零基础系统学（默认）**：基础篇 → 机器学习基础 → 神经网络 → 深度学习入门 → Transformer 深潜 → SVM 深潜 → 论文拆解 → 架构阐释 → DeepSeek 模型全谱。按 10–12 周排。

**直奔论文**：基础篇第 1–4 章 → Transformer 深潜（至少读注意力到解码器）→ 论文拆解 → 架构阐释 → 模型全谱。适合已经会 Python、只想尽快读懂 DeepSeek 报告的人。

**机器学习专项**：机器学习基础 → SVM 深潜 → 神经网络 → 深度学习入门。适合先打经典 ML 与神经网络基础、暂时不碰大模型论文的人。

## 怎么用

1. 双击根目录 `index.html`，先读“跨书总览”的推荐顺序。
2. 每章先看“一句话核心”和“学习目标”，再读讲解，最后做自测；低于 80% 就回到对应概念页。
3. 侧边栏“诊断”随机抽 5 题；答错会沿 `prerequisites` 依赖链倒推根因。
4. 高难概念页底部的“展开完整第一性原理推导”默认折叠，点开看逐步代数过程与数值算例。
5. 深潜课在 `07-transformer-deep/` 和 `08-svm-deep/`，自包含 HTML，保留原课的交互与内联公式。
6. 进度保存在浏览器本地，可导出/导入 JSON；各书进度独立。

## 目录结构

```
index.html                 总学习手册（单文件入口）
index.md                   Markdown 导航
00-跨书总览/               推荐顺序、概念映射、术语总表、节点地图、深潜专题、综合检验
01-foundations/            数学与 Transformer 骨架
04-machine-learning/       机器学习基础（周志华导读）
05-neural-networks/        神经网络从零
06-deep-learning/          深度学习入门（代码线）
07-transformer-deep/       Transformer 从零推导（深潜，自包含）
08-svm-deep/               SVM 从零推导（深潜，自包含）
02-paper-teardown/         R1 / V4 / V4.1 论文拆解
03-architecture/           三代架构阐释
09-deepseek-family/        DeepSeek 全家族：14 章 + 105+ 张模型卡索引
_build/                    合并、生成、CDN 修补、验证脚本
_work/                     论文 PDF 与过程数据（不推送公开仓库）
_merge_sources/            合并前的原仓库副本（只留在本地交付包，不推送公开仓库）
```

公开仓库只放站点、章节源码、manifest 与 `_build` 脚本；`_work/`、`_merge_sources/` 与 zip 由 `.gitignore` 排除，避免把论文 PDF 和第三方仓库副本一起推上去。

## 部署到 GitHub Pages

站点是纯静态文件，没有构建步骤。仓库根目录设为本目录内容，然后：

```bash
git init
git add -A
git commit -m "AI 架构学习系统"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

仓库 Settings → Pages → Source 选 `Deploy from a branch`，Branch 选 `main`，目录选 `/ (root)`，保存后等 1–2 分钟。

`.nojekyll` 必须保留，否则 GitHub Pages 的 Jekyll 会忽略以下划线开头的目录，中文文件名也可能出问题。

## 已知边界

- 公式用 KaTeX、图用 Mermaid，均走 CDN；离线时文字和导航仍可用，公式会显示成源码。页面已把 npmmirror 放在首选，并给 KaTeX 加载加了 4–5 秒超时回退。
- 内容是基于公开论文、公开代码与公开教材整理的 learning notes，不是官方教材；数字以论文原文为准。
- 自动验证结果与同义召回断言的说明见 `交付说明.md`。
- 原仓库 `SVM`、`transformer`、`neural-net-zero` 未被修改；本仓库是合并后的学习站点。

## 论文来源

- DeepSeek-R1: `https://arxiv.org/abs/2501.12948`
- DeepSeek-V4: `https://arxiv.org/abs/2606.19348`
- DeepSeek-V4.1: `https://arxiv.org/abs/2609.19969`
- DeepSeek-V3（背景参考）: `https://arxiv.org/abs/2412.19437`
