#!/usr/bin/env python3
"""把总入口首页换成一条 7 步主线，资料库降级为折叠区。"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

OLD = """  let pre='';
  if(docId===FIRST_DOC){
    pre = '<h1>学习总手册</h1>'
      + '<p>本学习系统把书点化为一套可跟着走的学习内容。顶部切换书籍，或用下方卡片进入；'
      + '每本书含学习路径、章节精讲、概念页、测验、抽认卡、术语表、模式库与速查表，进度自动保存在本机浏览器。</p>'
      + '<div class="book-cards">'
      + META.map(m=>`<div class="book-card"><h3>${esc(m.title)}</h3>
          <div class="meta">${m.chapters} 章 · ${m.concepts} 概念 · ${m.quizzes} 测验 · ${m.cards} 抽认卡</div>
          <div class="enter"><a href="#/book/${m.key}/path">进入学习 →</a> &nbsp;|&nbsp;
          <a href="${encodeURI(m.companion)}" target="_blank">单独伴侣 ↗</a></div></div>`).join('')
      + '</div>';
  }"""

NEW = """  let pre='';
  if(docId===FIRST_DOC){
    const steps=[
      {n:'01',t:'先把地基补到够用',d:'矩阵乘法、softmax、注意力、FFN。只看这四件事，不从头学完整本数学。',b:'deepseek-foundations',x:'基础篇 6 章 · 约 6 小时'},
      {n:'02',t:'看懂 Transformer 一层',d:'Q/K/V、多头、残差、LayerNorm。先能手画一层，再读论文。',b:'deepseek-foundations',x:'基础篇第 4–5 章 + Transformer 深潜'},
      {n:'03',t:'读三篇论文',d:'R1、V4、V4.1 按“问题—方法—数据—实验—局限”拆，不背结论。',b:'deepseek-papers',x:'论文拆解 5 章 · 约 5 小时'},
      {n:'04',t:'拆三代架构',d:'V3/R1、V4、V4.1 的瓶颈、机制、代价。每章先问“不改会怎样”。',b:'deepseek-architecture',x:'架构阐释 5 章 · 约 4 小时'},
      {n:'05',t:'走一遍全家族',d:'从 dense 到 V4.1，12 章。每代只记一个结构件，不背模型名。',b:'deepseek-family',x:'模型全谱 12 章 · 约 12 小时'},
      {n:'06',t:'选型与成本',d:'按任务、显存、延迟、上下文、许可证做决策；手算 KV 账。',b:'deepseek-family',x:'第 11 章 + 架构篇第 14 章'},
      {n:'07',t:'按需补课',d:'机器学习、神经网络、深度学习、SVM 是资料库，遇到缺口再查，不按顺序读。',b:'machine-learning',x:'04 / 05 / 06 / 08 资料库'},
    ];
    pre='<div class="hero"><h1>AI 架构学习：一条主线走完</h1>'
      +'<p>如果你只想按顺序学，按下面 7 步走。每一步只读一章或一小节，先拿结论，再进书里看推导。数学和代码接近零基础也能走，但第 4、5、8、9 章的数字要动手算一遍。</p></div>'
      +'<div class="simple-path">'
      + steps.map(s=>`<div class="step-card"><div class="step-num">${s.n}</div><div><h3>${esc(s.t)}</h3><p>${esc(s.d)}</p><div class="step-links"><a href="#/book/${s.b}/path">进入：${esc(s.x)}</a>${s.n==='05'?'<a href="#/book/deepseek-family/chapter/ch01">先读家族地图</a>':''}${s.n==='06'?'<a href="#/book/deepseek-family/chapter/ch11">先读选型表</a>':''}</div></div></div>`).join('')
      +'</div>'
      +'<div class="library"><h2>资料库</h2><p>下面这些书不用从头读到尾。主线卡住时，按关键词回来查。</p><div class="lib-grid">'
      + META.map(m=>`<a class="lib-item" href="#/book/${m.key}/path"><b>${esc(m.title)}</b><span>${m.chapters} 章 · ${m.quizzes} 测验</span></a>`).join('')
      + `<a class="lib-item" href="${encodeURI('07-transformer-deep/index.html')}" target="_blank"><b>Transformer 深潜</b><span>15 节 · 179 个推导步骤</span></a>`
      + `<a class="lib-item" href="${encodeURI('08-svm-deep/index.html')}" target="_blank"><b>SVM 深潜</b><span>16 节 · 1355 个公式</span></a>`
      + `<a class="lib-item" href="${encodeURI('10-backprop-deep/index.html')}" target="_blank"><b>反向传播与优化器</b><span>10 节 · 手算梯度到 Adam</span></a>`
      + `<a class="lib-item" href="${encodeURI('11-moe-mla-deep/index.html')}" target="_blank"><b>MoE 与 MLA</b><span>10 节 · 路由与 KV 账</span></a>`
      + `<a class="lib-item" href="${encodeURI('12-probability-eval-deep/index.html')}" target="_blank"><b>概率、损失与评估</b><span>10 节 · 交叉熵 / PR / AUC</span></a>`
      + `<a class="lib-item" href="${encodeURI('13-train-infer-deep/index.html')}" target="_blank"><b>训练与推理账本</b><span>9 节 · FLOPs / KV / 并行</span></a>`
      +'</div></div>';
  }"""

CSS = """
.hero{padding:6px 0 2px}
.hero h1{font-size:clamp(1.65rem,4vw,2.45rem);line-height:1.18;margin:0 0 10px}
.hero p{max-width:780px;color:var(--muted);font-size:1.02rem;margin:0}
.simple-path{display:grid;gap:12px;margin:22px 0 28px}
.step-card{display:grid;grid-template-columns:52px 1fr;gap:14px;border:1px solid var(--border);border-radius:14px;padding:16px;background:var(--panel)}
.step-num{font-weight:800;font-size:1.35rem;color:var(--accent);line-height:1.2;letter-spacing:-.02em}
.step-card h3{margin:0 0 5px;font-size:1.02rem}
.step-card p{margin:0 0 10px;color:var(--muted);line-height:1.65;font-size:.96rem}
.step-links{display:flex;flex-wrap:wrap;gap:8px}
.step-links a{font-size:.9rem;padding:5px 10px;border-radius:999px;border:1px solid var(--border);background:var(--accent-soft);color:var(--text);text-decoration:none}
.step-links a:hover{border-color:var(--accent);text-decoration:none}
.library{margin-top:8px;border-top:1px solid var(--border);padding-top:18px}
.library h2{font-size:1.12rem;margin:0 0 4px}
.library p{color:var(--muted);font-size:.94rem;margin:0 0 12px}
.lib-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.lib-item{display:flex;flex-direction:column;gap:2px;border:1px solid var(--border);border-radius:10px;padding:10px 12px;background:var(--bg);text-decoration:none;color:var(--text)}
.lib-item b{font-size:.94rem;line-height:1.4}
.lib-item span{font-size:.8rem;color:var(--muted)}
.lib-item:hover{border-color:var(--accent);text-decoration:none}
@media(max-width:820px){
  .step-card{grid-template-columns:42px 1fr;gap:10px;padding:13px}
  .step-num{font-size:1.1rem}
  .lib-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:420px){.lib-grid{grid-template-columns:1fr}}
"""

def main():
    text = INDEX.read_text(encoding="utf-8")
    if OLD not in text:
        print("未找到旧首页块；可能已改过。")
        return 1
    text = text.replace(OLD, NEW, 1)
    marker = "@media print{"
    if CSS.strip() not in text:
        if marker not in text:
            print("未找到 CSS 插入点")
            return 1
        text = text.replace(marker, CSS + "\n" + marker, 1)
    INDEX.write_text(text, encoding="utf-8")
    print("✓ 首页改为 7 步主线")
    return 0

if __name__ == "__main__":
    sys.exit(main())
