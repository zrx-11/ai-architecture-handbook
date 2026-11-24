#!/usr/bin/env python3
"""把总入口首页换成一条 8 步主线，资料库按需展开。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

NEW_BLOCK = r"""  let pre='';
  if(docId===FIRST_DOC){
    const deep=[
      ['14-math-deep','数学基础','12 节','函数 / 向量 / 矩阵 / 导数 / 概率'],
      ['15-python-deep','Python 与 NumPy','10 节','变量 / 函数 / 形状 / 广播 / 手写梯度'],
      ['16-classical-ml-deep','经典机器学习','12 节','回归 / 树 / 聚类 / PCA / 评估'],
      ['17-cnn-rnn-deep','CNN 与 RNN','10 节','卷积 / 池化 / 残差 / LSTM / 注意力'],
      ['18-rl-grpo-deep','强化学习与 GRPO','10 节','MDP / 策略梯度 / PPO / 组内优势'],
      ['19-deepseek-arch-deep','DeepSeek 架构深潜','13 节','MoE / MLA / DSA / CSA / V4.1'],
      ['20-multimodal-deep','多模态模型','9 节','ViT / CLIP / VL / Janus / OCR'],
      ['21-eval-safety-deep','评测与安全','9 节','pass@k / 裁判偏差 / 幻觉 / 红队'],
      ['22-serving-deep','推理部署','9 节','KV / PagedAttention / 批处理 / 并行'],
      ['07-transformer-deep','Transformer 深潜','15 节','从初中数学推到一层 Transformer'],
      ['08-svm-deep','SVM 深潜','16 节','最大间隔 / 对偶 / KKT / 核技巧'],
      ['10-backprop-deep','反向传播与优化器','10 节','计算图 / 链式法则 / Adam'],
      ['11-moe-mla-deep','MoE 与 MLA','10 节','路由 / 共享专家 / KV 账 / DSA'],
      ['12-probability-eval-deep','概率、损失与评估','10 节','交叉熵 / P-R-F1 / AUC / 泄漏'],
      ['13-train-infer-deep','训练与推理账本','9 节','6ND / KV / prefill-decode / 量化'],
    ];
    const steps=[
      {n:'01',t:'数学与编程工具',d:'先补到能算、能写：向量、矩阵、导数、链式法则、概率；再到 Python/NumPy 的形状、广播和手写梯度。每节都有可手算例子，不要求先学完整本数学。',p:'14-math-deep/index.html',pl:'数学基础 12 节',x:[['15-python-deep/index.html','Python 10 节'],['#/book/machine-learning/chapter/ch01','机器学习第 1 章']]},
      {n:'02',t:'AI 全景与机器学习',d:'先用 Hello AI 建立 AI 全景，再用 AIMA 补搜索、知识、不确定性与决策；回到周志华和神经网络，理解模型到底在优化什么。',p:'#/book/hello-ai/path',pl:'AI 导论 20 章',x:[['#/book/aima4/path','AIMA 28 章'],['#/book/machine-learning/path','机器学习 16 章'],['#/book/neural-networks/path','神经网络 13 章'],['10-backprop-deep/index.html','反向传播 10 节']]},
      {n:'03',t:'深度学习与序列模型',d:'从感知机、两层网络到正则化与 CNN；再用 RNN/LSTM/seq2seq 对照，理解为什么序列建模最终转向注意力。',p:'#/book/deep-learning-scratch/path',pl:'深度学习入门 8 章',x:[['17-cnn-rnn-deep/index.html','CNN/RNN 10 节'],['#/book/d2l/path','动手学深度学习 11 章'],['#/book/deepseek-foundations/path','Transformer 基础 6 章']]},
      {n:'04',t:'Transformer 与论文阅读',d:'Q/K/V、多头、残差、LayerNorm、FFN；用 shape 变化读懂一层 Transformer，再按“问题—方法—数据—实验—局限”拆 DeepSeek R1/V4/V4.1 三篇样例论文。',p:'#/book/deepseek-foundations/path',pl:'基础篇 6 章',x:[['07-transformer-deep/index.html','Transformer 深潜 15 节'],['#/book/deepseek-papers/path','论文拆解 5 章']]},
      {n:'05',t:'案例架构：DeepSeek 三代',d:'把 DeepSeek 当作第一个完整案例：MoE、MLA、MTP、DSA、CSA/HCA、mHC/Muon、Engram/DSpark；从 dense 走到 V4.1，再看 VL/Janus/OCR 多模态分支。',p:'19-deepseek-arch-deep/index.html',pl:'架构深潜 13 节',x:[['#/book/deepseek-architecture/path','架构阐释 5 章'],['#/book/deepseek-family/path','模型全谱 14 章'],['20-multimodal-deep/index.html','多模态 9 节']]},
      {n:'06',t:'全球开放模型对照',d:'把同一套读法用到 Llama、Qwen、Mistral、Gemma、Phi、GLM、Kimi、MiniMax、InternLM 等家族；读 config、算参数与 KV、看许可证，知道 DeepSeek 之外还有什么路线。',p:'#/book/global-open-models/path',pl:'全球分册 16 章',x:[['11-moe-mla-deep/index.html','MoE/MLA 10 节'],['#/book/global-open-models/chapter/ch16','101 行模型索引'],['#/book/global-open-models/chapter/ch14','许可证与评测']]},
      {n:'07',t:'从零实现一次 LLM',d:'把 tokenizer、tiny GPT、预训练、SFT、LoRA、偏好对齐、KV cache、RAG 与评测串成一条可验收的链路。先跑 CPU 小实验，再按单卡/云选择路线；每章都有形状账本和检查点。',p:'#/book/llm-from-scratch/path',pl:'LLM 从零实现 14 章',x:[['13-train-infer-deep/index.html','训练账本 9 节'],['18-rl-grpo-deep/index.html','RL/GRPO 10 节'],['22-serving-deep/index.html','推理部署 9 节']]},
      {n:'08',t:'训练、评测与部署',d:'MDP、策略梯度、PPO/GRPO；再算 FLOPs、KV、并行和量化，做 pass@k、裁判偏差、幻觉与红队，最后到 PagedAttention、continuous batching 与 SLA。',p:'22-serving-deep/index.html',pl:'推理部署 9 节',x:[['18-rl-grpo-deep/index.html','强化学习 10 节'],['#/book/rl-sutton/path','Sutton 强化学习 17 章'],['13-train-infer-deep/index.html','训练账本 9 节'],['21-eval-safety-deep/index.html','评测安全 9 节'],['#/book/ai-mechanisms-formulas/path','机制公式总库 11 章']]},
    ];
    pre='<div class="hero"><div class="hero-kicker">AI 架构学习手册 · 14 本分册 · 15 套深潜课 · 7 个资料馆</div>'
      +'<h1>从数学基础，到主流大模型架构</h1>'
      +'<p>数学和代码接近零基础也能走。主线只有 8 步：先补数学与 Python，再经过机器学习、神经网络、深度学习、Transformer 与论文阅读；DeepSeek 是第一个完整案例，全球开放模型是扩展对照，最后从零跑通一次 tiny LLM。</p>'
      +'<div class="hero-stats"><span><b>14</b> 本分册</span><span><b>15</b> 套深潜课</span><span><b>164</b> 节单点推导</span><span><b>184</b> 章系统课</span></div></div>'
      +'<div class="path-head"><h2>学习路径</h2><p>按顺序点。每步先读主入口，再用右侧小标签补缺口。</p></div>'
      +'<div class="simple-path">'
      + steps.map(s=>`<div class="step-card"><div class="step-num">${s.n}</div><div><h3>${esc(s.t)}</h3><p>${esc(s.d)}</p><div class="step-links"><a class="primary" href="${encodeURI(s.p)}">${esc(s.pl)} →</a>${s.x.map(x=>`<a href="${encodeURI(x[0])}">${esc(x[1])}</a>`).join('')}</div></div></div>`).join('')
      +'</div>'
      +'<details class="library"><summary><span>资料库</span><em>14 本分册 · 15 套深潜课 · 专题页</em></summary>'
      +'<p class="lib-note">主线卡住时按关键词回来查。分册负责广度、依赖顺序和诊断；深潜课负责单点推到底。</p>'
      +'<h3>分册</h3><div class="lib-grid">'
      + META.map(m=>`<a class="lib-item book-card" href="#/book/${m.key}/path"><b>${esc(m.title)}</b><span>${m.chapters} 章 · ${m.quizzes} 测验</span></a>`).join('')
      +'</div><h3>深潜课</h3><div class="lib-grid deep">'
      + deep.map(d=>`<a class="lib-item" href="${encodeURI(d[0]+'/index.html')}" target="_blank"><b>${esc(d[1])}</b><span>${esc(d[2])} · ${esc(d[3])}</span></a>`).join('')
      +'</div><h3>专题</h3><div class="lib-grid topics">'
      + `<a class="lib-item" href="#/cross/doc7"><b>知识覆盖地图</b><span>哪些节点覆盖了、哪些还是缺口</span></a>`
      + `<a class="lib-item" href="#/cross/doc4"><b>学习节点地图</b><span>依赖主线与三条路线推进表</span></a>`
      + `<a class="lib-item" href="#/cross/doc6"><b>深潜专题</b><span>15 套课怎么选、怎么配主线</span></a>`
      + `<a class="lib-item" href="#/cross/doc2"><b>跨书概念映射</b><span>同一概念在不同分册的讲法</span></a>`
      + `<a class="lib-item" href="#/cross/doc3"><b>综合检验</b><span>跨书任务与进阶路线</span></a>`
      + `<a class="lib-item" href="#/cross/doc8"><b>三条学习路线</b><span>零基础 24 周 / 工程师 12 周 / 研究 16 周</span></a>`
      + `<a class="lib-item" href="#/cross/doc9"><b>开源项目地图</b><span>该读、该跑、只该看的 14 个项目</span></a>`
      +'</div></details>'
      +'<details class="library"><summary><span>同源资料馆</span><em>7 个扩展库</em></summary>'
      +'<p class="lib-note">从你名下的重合项目里挑出来的扩展材料。它们保留原有单文件结构，不挤占主线；需要查机理、课程地图、模型清单或数学先修时再打开。</p>'
      +'<div class="lib-grid topics">'
      + `<a class="lib-item" href="${encodeURI('29-ai-study-notes/HTML版/AI机理深度研习系列.html')}" target="_blank"><b>AI 机理深研 126 讲</b><span>Transformer 30 讲 / 信息论 / Agent / 运筹</span></a>`
      + `<a class="lib-item" href="${encodeURI('30-llm-model-catalog/index.html')}" target="_blank"><b>全球大模型清单 306 个</b><span>25 家厂商 / 2026-11 / 参数与许可证</span></a>`
      + `<a class="lib-item" href="${encodeURI('31-probability-statistics/概率统计从零推导.html')}" target="_blank"><b>概率统计从零推导 27 章</b><span>从初中概率到假设检验</span></a>`
      + `<a class="lib-item" href="${encodeURI('32-math-basics/index.html')}" target="_blank"><b>数学基础知识丛书 24 本</b><span>有理数到微积分的先修库</span></a>`
      + `<a class="lib-item" href="${encodeURI('33-agentic-design-patterns/index.html')}" target="_blank"><b>智能体设计模式 26 章</b><span>Agent 模式 / RAG / 反思 / 多智能体</span></a>`
      + `<a class="lib-item" href="https://zrx-11.github.io/AI-courses/" target="_blank"><b>AI 课程地图 20 门</b><span>课程选课导航与术语词典</span></a>`
      + `<a class="lib-item" href="https://zrx-11.github.io/ai-history-site/" target="_blank"><b>AI 简史 500+ 板块</b><span>24 个历史节点 / 论文与人物</span></a>`
      +'</div></details>';
  }
"""

CSS = r"""
.hero{padding:8px 0 4px}
.hero-kicker{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:8px}
.hero h1{font-size:clamp(1.7rem,4vw,2.5rem);line-height:1.16;margin:0 0 10px}
.hero p{max-width:820px;color:var(--muted);font-size:1.02rem;margin:0 0 14px;line-height:1.7}
.hero-stats{display:flex;flex-wrap:wrap;gap:10px 18px;font-size:.88rem;color:var(--muted)}
.hero-stats b{color:var(--text);font-size:1.08rem;margin-right:3px}
.path-head{margin:24px 0 12px}
.path-head h2{font-size:1.18rem;margin:0 0 4px}
.path-head p{color:var(--muted);font-size:.92rem;margin:0}
.simple-path{display:grid;gap:12px;margin:0 0 26px}
.step-card{display:grid;grid-template-columns:52px 1fr;gap:14px;border:1px solid var(--border);border-radius:14px;padding:16px;background:var(--panel)}
.step-num{font-weight:800;font-size:1.35rem;color:var(--accent);line-height:1.2;letter-spacing:-.02em}
.step-card h3{margin:0 0 5px;font-size:1.04rem}
.step-card p{margin:0 0 10px;color:var(--muted);line-height:1.68;font-size:.95rem}
.step-links{display:flex;flex-wrap:wrap;gap:8px}
.step-links a{font-size:.88rem;padding:5px 10px;border-radius:999px;border:1px solid var(--border);background:var(--accent-soft);color:var(--text);text-decoration:none}
.step-links a.primary{background:var(--accent);color:#fff!important;border-color:var(--accent);font-weight:600}
.step-links a:hover{border-color:var(--accent);text-decoration:none}
.library{margin-top:6px;border-top:1px solid var(--border);padding-top:16px}
.library summary{cursor:pointer;list-style:none;display:flex;flex-wrap:wrap;align-items:baseline;gap:8px}
.library summary::-webkit-details-marker{display:none}
.library summary span{font-size:1.12rem;font-weight:700}
.library summary em{font-style:normal;font-size:.82rem;color:var(--muted)}
.library[open] summary{margin-bottom:8px}
.lib-note{color:var(--muted);font-size:.92rem;margin:0 0 14px;line-height:1.65}
.library h3{font-size:.98rem;margin:16px 0 8px;color:var(--muted)}
.lib-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.lib-item{display:flex;flex-direction:column;gap:3px;border:1px solid var(--border);border-radius:10px;padding:10px 12px;background:var(--bg);text-decoration:none;color:var(--text)}
.lib-item b{font-size:.93rem;line-height:1.4}
.lib-item span{font-size:.78rem;color:var(--muted);line-height:1.5}
.lib-item:hover{border-color:var(--accent);text-decoration:none}
@media(max-width:820px){
  .step-card{grid-template-columns:42px 1fr;gap:10px;padding:13px}
  .step-num{font-size:1.1rem}
  .lib-grid{grid-template-columns:1fr 1fr}
  .hero-stats{gap:8px 14px}
}
@media(max-width:420px){.lib-grid{grid-template-columns:1fr}}
"""

def main():
    text = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r"  let pre='';\n  if\(docId===FIRST_DOC\)\{.*?\n  \}\n  v\.innerHTML", re.S)
    if not pat.search(text):
        print("未找到首页块；可能已改过。")
        return 1
    text = pat.sub(NEW_BLOCK + "  v.innerHTML", text, count=1)
    text = text.replace(
        'const html=CROSS[docId]||\'<div class="empty">页面不存在</div>\';',
        'const html=docId===FIRST_DOC?\'\':(CROSS[docId]||\'<div class="empty">页面不存在</div>\');',
        1,
    )
    marker = "@media print{"
    if CSS.strip() not in text:
        if marker not in text:
            print("未找到 CSS 插入点")
            return 1
        text = text.replace(marker, CSS + "\n" + marker, 1)
    text = text.replace("<title>学习总手册</title>",
        "<title>AI 架构学习手册 · 从数学与编程基础到主流大模型架构</title>", 1)
    text = text.replace("<span class=\"brand\">学习总手册<span>点化学习系统 · 统一入口</span></span>",
        "<span class=\"brand\">AI 架构学习手册<span>从数学与编程基础到主流大模型架构</span></span>", 1)
    text = text.replace("<h1>学习总手册</h1>", "<h1>AI 架构学习手册</h1>", 1)
    INDEX.write_text(text, encoding="utf-8")
    print("✓ 首页改为全栈 8 步主线 + 可展开资料库")
    return 0

if __name__ == "__main__":
    sys.exit(main())
