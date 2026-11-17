# DeepSeek 架构学习系统

**在线访问**：<https://zrx-11.github.io/deepseek-architecture-learning/>  
**仓库**：<https://github.com/zrx-11/deepseek-architecture-learning>

给数学和代码接近零基础的学习者，把 DeepSeek-R1、DeepSeek-V4、DeepSeek-V4.1 三篇技术报告拆成一套能按依赖顺序学、答错能倒推根因、难点能展开完整推导的交互式学习手册。

## 先说明一个事实

DeepSeek 更准确的说法是**开放权重**，不是“全部开源”：模型权重、技术报告、部分推理与训练框架代码公开；完整训练数据、数据清洗流程和端到端训练流水线没有公开。架构层面（`modeling_deepseek.py`、`configuration_deepseek.py` 里的 MLA、DeepSeekMoE、MTP 等结构）是公开且可复现的，但“架构开源”不等于“整个模型全流程开源”。本学习系统讲的是公开技术报告和公开代码里能核对的部分。

## 这套材料有什么

| 分册 | 内容 | 规模 |
|---|---|---|
| 基础篇：从零到 Transformer | 向量、矩阵、softmax、参数与梯度、注意力、Transformer 一层楼、V3 的 MLA/MoE/MTP 地基 | 5 章 / 16 概念 / 3 个深度推导 |
| 论文拆解：R1 / V4 / V4.1 | 按“问题—方法—数据—实验—局限”逐篇拆 R1、V4、V4.1 | 4 章 / 15 概念 / 5 个深度推导 |
| 架构阐释：三代模型的设计逻辑 | 瓶颈迁移、组件演进、训练路线、选型与取舍 | 4 章 / 5 概念 |

合计 13 章、36 个概念页、39 道测验、52 张抽认卡、69 条术语、8 个第一性原理深度推导片段。

## 怎么用

1. 双击根目录 `index.html`，从“跨书总览”开始，按推荐顺序进入三本书。
2. 每章先看“一句话核心”和“学习目标”，再读讲解，最后做自测；低于 80% 就回到对应概念页。
3. 侧边栏有诊断测试：答错会沿 `prerequisites` 依赖链倒推，指出可能的根因概念。
4. 高难概念页底部有“展开完整第一性原理推导”，默认折叠，点开看逐步代数过程与数值算例。
5. 进度保存在浏览器本地，可导出/导入 JSON；换设备时带走 JSON 即可。

## 目录结构

```
index.html                 总学习手册（单文件入口）
index.md                   Markdown 导航
00-跨书总览/               推荐顺序、跨书概念映射、综合检验
01-foundations/            基础篇：章节、概念、测验、卡片、术语、manifest、单书伴侣
02-paper-teardown/         论文拆解篇（同上）
03-architecture/           架构阐释篇（同上）
_build/                    构建脚本、CDN 修补脚本、验证报告
_work/                     论文 PDF、抽取与过程数据
```

## 部署到 GitHub Pages

站点是纯静态文件，没有构建步骤。把仓库根目录设为本目录内容，然后：

```bash
git init
git add -A
git commit -m "DeepSeek 架构学习系统"
git branch -M main
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
```

仓库 Settings → Pages → Source 选 `Deploy from a branch`，Branch 选 `main`，目录选 `/ (root)`，保存后等 1–2 分钟，访问 `https://<用户名>.github.io/<仓库名>/`。

`.nojekyll` 必须保留，否则 GitHub Pages 的 Jekyll 会忽略以下划线开头的目录，中文文件名也可能出问题。

## 已知边界

- 公式用 KaTeX、图用 Mermaid，均走 CDN；离线时文字和导航仍可用，公式会显示成源码。页面已把 npmmirror 放在首选，并给 KaTeX 加载加了 4–5 秒超时回退。
- 内容是基于公开论文和公开代码整理的学习笔记，不是 DeepSeek 官方教材；数字以论文原文为准，遇到版本差异以原报告为准。
- 自动验证 43/44 通过。唯一失败项是验证脚本把“定义”当成书中缺失词，实际索引里存在“定义”，所以只走精确命中、不会标“同义”；手动用“释义”复验，同义召回 40 条全部带同义标记，功能正常。详见 `交付说明.md`。

## 论文来源

- DeepSeek-R1: `https://arxiv.org/abs/2501.12948`
- DeepSeek-V4: `https://arxiv.org/abs/2606.19348`
- DeepSeek-V4.1: `https://arxiv.org/abs/2609.19969`
- DeepSeek-V3（背景参考）: `https://arxiv.org/abs/2412.19437`
