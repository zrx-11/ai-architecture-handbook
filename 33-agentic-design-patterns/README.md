# 智能体设计模式 · 点化学习系统

把《智能体设计模式：智能系统构建实战指南》（305 页中文 PDF）做成一套可直接开学的知识库：26 章精讲、11 篇跨章概念、77 条术语、58 道题、52 张抽认卡，收在一个离线可开的 `index.html` 里。

## 怎么打开

双击 `index.html`。所有内容内嵌在这一个文件里，不需要联网（Mermaid 图示在线时自动渲染，离线时显示源码 + 文字说明）。

## 目录

| 路径 | 说明 |
|---|---|
| `index.html` | 总入口：书切换、导航、搜索、测验、抽认卡、进度 |
| `index.md` | 同一份内容的 Markdown 导航 |
| `01-智能体设计模式/` | 单书知识库 + 单书伴侣 HTML + manifest |
| `01-智能体设计模式/chapters/` | 26 章精讲（ch00–ch25） |
| `01-智能体设计模式/concepts/` | 11 篇跨章概念页 |
| `01-智能体设计模式/patterns.md` | 21 个模式 + 8 条决策规则 + 11 个反模式 |
| `01-智能体设计模式/cheatsheet.md` | 公式、判据、参数经验值、错误对照 |
| `01-智能体设计模式/paths/learn.md` | 12 步学习路径（按依赖拓扑） |
| `01-智能体设计模式/_work/` | 抽取语料、题库、卡片数据、验证报告 |
| `从零推导-RAG.html` | 深推页：RAG 从向量夹角推到检索工程 |
| `从零推导-反思.html` | 深推页：反思从控制结构推到退化路径 |

## 在线地址

- 站点：https://zrx-11.github.io/agentic-design-patterns-handbook/
- 仓库：https://github.com/zrx-11/agentic-design-patterns-handbook

原书全文抽取文本（`01-智能体设计模式/_work/raw/`）已通过 `.gitignore` 排除，不随仓库公开。

## 部署到 GitHub Pages

1. 把本目录下所有文件（含 `.nojekyll`）推到仓库根目录：
   ```bash
   git add .
   git commit -m "add study handbook"
   git push origin main
   ```
2. 仓库 Settings → Pages → Source 选 `Deploy from a branch`,分支 `main`,目录 `/ (root)`,Save。
3. 等 1~2 分钟，访问 `https://<用户名>.github.io/<仓库名>/`。

`.nojekyll` 的作用是关闭 Jekyll：否则以下划线开头的目录（`_work/`、`_build/`）会被丢弃，中文目录名也可能出问题。

若用自定义域名，在同目录加 `CNAME` 文件，内容写域名。

## 已知限制

- Mermaid 依赖 CDN，纯离线环境下图区显示源码；每张图下方都配了文字说明，不影响阅读。
- 数学公式在知识库正文里统一转为纯文本（伴侣渲染器不支持 KaTeX）；只有两页深推页内联了 KaTeX 与字体。
- 进度保存在浏览器 localStorage，换浏览器或清缓存会重置。

## 内容说明

原书 PDF 未署名作者（元数据 author 仅为占位），在线阅读地址：https://jimmysong.io/zh/book/agentic-design-patterns/ 。本知识库为学习用途的二次整理，不替代原书。
