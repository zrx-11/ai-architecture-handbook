#!/usr/bin/env python3
"""把生成页面的 CDN 顺序改为国内优先，并给 KaTeX 加载加超时回退。

知枢 skill 的踩坑清单第 5、11 条要求：国内 jsDelivr 可能长时间不回调，
必须 npmmirror 优先、每个源带超时。build_companion.py / build_handbook.py
当前产物仍是 jsDelivr 优先，这里做一次交付前后处理，不改 skill 源文件。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    ROOT / "01-foundations/deepseek-foundations学习伴侣.html",
    ROOT / "02-paper-teardown/deepseek-papers学习伴侣.html",
    ROOT / "03-architecture/deepseek-architecture学习伴侣.html",
    ROOT / "04-machine-learning/machine-learning学习伴侣.html",
    ROOT / "05-neural-networks/neural-networks学习伴侣.html",
    ROOT / "06-deep-learning/deep-learning学习伴侣.html",
    ROOT / "index.html",
]

KATEX_CSS = """const cssUrls = [
    'https://registry.npmmirror.com/katex/0.16.9/files/dist/katex.min.css',
    'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
    'https://unpkg.com/katex@0.16.9/dist/katex.min.css'
  ];"""

KATEX_JS = """const jsUrls = [
    'https://registry.npmmirror.com/katex/0.16.9/files/dist/katex.min.js',
    'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js',
    'https://unpkg.com/katex@0.16.9/dist/katex.min.js'
  ];"""

MERMAID = """const urls=['https://registry.npmmirror.com/mermaid/10.9.1/files/dist/mermaid.min.js',
              'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js',
              'https://unpkg.com/mermaid@10.9.1/dist/mermaid.min.js'];"""

KATEX_CSS_TIGHT = """const cssUrls=[
    'https://registry.npmmirror.com/katex/0.16.9/files/dist/katex.min.css',
    'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css',
    'https://unpkg.com/katex@0.16.9/dist/katex.min.css'
  ];"""

KATEX_JS_TIGHT = """const jsUrls=[
    'https://registry.npmmirror.com/katex/0.16.9/files/dist/katex.min.js',
    'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js',
    'https://unpkg.com/katex@0.16.9/dist/katex.min.js'
  ];"""

LOADER_TIGHT = """const tryCss=()=>{
    if(ci>=cssUrls.length){ tryJs(); return; }
    const link=document.createElement('link');
    link.rel='stylesheet'; link.href=cssUrls[ci++];
    let settled=false, timer=null;
    const next=()=>{ if(settled) return; settled=true; clearTimeout(timer); link.remove(); tryCss(); };
    timer=setTimeout(next,4000);
    link.onload=()=>{ if(settled) return; settled=true; clearTimeout(timer); tryJs(); };
    link.onerror=next;
    document.head.appendChild(link);
  };
  const tryJs=()=>{
    if(ji>=jsUrls.length){ katexLoading=false; return; }
    const s=document.createElement('script');
    s.src=jsUrls[ji++];
    let settled=false, timer=null;
    const next=()=>{ if(settled) return; settled=true; clearTimeout(timer); s.onload=null; s.onerror=null; s.remove(); tryJs(); };
    timer=setTimeout(next,5000);
    s.onload=()=>{ if(settled) return; settled=true; clearTimeout(timer); katexReady=true; katexLoading=false; doRenderMath(); };
    s.onerror=next;
    document.head.appendChild(s);
  };
  tryCss();"""

LOADER = """const tryCss = () => {
    if(ci >= cssUrls.length){ tryJs(); return; }
    const link = document.createElement('link');
    link.rel = 'stylesheet'; link.href = cssUrls[ci++];
    let settled = false, timer = null;
    const next = () => {
      if(settled) return;
      settled = true; clearTimeout(timer); link.remove(); tryCss();
    };
    timer = setTimeout(next, 4000);
    link.onload = () => {
      if(settled) return;
      settled = true; clearTimeout(timer); tryJs();
    };
    link.onerror = next;
    document.head.appendChild(link);
  };
  const tryJs = () => {
    if(ji >= jsUrls.length){ katexLoading = false; return; }
    const s = document.createElement('script');
    s.src = jsUrls[ji++];
    let settled = false, timer = null;
    const next = () => {
      if(settled) return;
      settled = true; clearTimeout(timer); s.onload = null; s.onerror = null; s.remove(); tryJs();
    };
    timer = setTimeout(next, 5000);
    s.onload = () => {
      if(settled) return;
      settled = true; clearTimeout(timer); katexReady = true; katexLoading = false; doRenderMath();
    };
    s.onerror = next;
    document.head.appendChild(s);
  };
  tryCss();"""


def patch(text: str) -> tuple[str, list[str]]:
    notes = []
    if "const cssUrls = [" in text:
        text, n = re.subn(r"const cssUrls = \[.*?\];", KATEX_CSS, text, count=1, flags=re.S)
        notes.append(f"katex css order: {n}")
    elif "const cssUrls=[" in text:
        text, n = re.subn(r"const cssUrls=\[.*?\];", KATEX_CSS_TIGHT, text, count=1, flags=re.S)
        notes.append(f"katex css order(tight): {n}")
    if "const jsUrls = [" in text:
        text, n = re.subn(r"const jsUrls = \[.*?\];", KATEX_JS, text, count=1, flags=re.S)
        notes.append(f"katex js order: {n}")
    elif "const jsUrls=[" in text:
        text, n = re.subn(r"const jsUrls=\[.*?\];", KATEX_JS_TIGHT, text, count=1, flags=re.S)
        notes.append(f"katex js order(tight): {n}")
    if "mermaid.min.js" in text:
        text, n = re.subn(
            r"const urls=\['https://cdn\.jsdelivr\.net/npm/mermaid@10\.9\.1/dist/mermaid\.min\.js',\s*"
            r"'https://registry\.npmmirror\.com/mermaid/10\.9\.1/files/dist/mermaid\.min\.js',\s*"
            r"'https://unpkg\.com/mermaid@10\.9\.1/dist/mermaid\.min\.js'\];",
            MERMAID, text, count=1, flags=re.S)
        notes.append(f"mermaid order: {n}")
    if "const tryCss = () => {" in text:
        text, n = re.subn(
            r"const tryCss = \(\) => \{.*?\n\s*tryCss\(\);",
            LOADER, text, count=1, flags=re.S)
        notes.append(f"katex timeout loader: {n}")
    elif "const tryCss=()=>{" in text:
        text, n = re.subn(
            r"const tryCss=\(\)=>\{.*?\n\s*tryCss\(\);",
            LOADER_TIGHT, text, count=1, flags=re.S)
        notes.append(f"katex timeout loader(tight): {n}")
    return text, notes


def main() -> int:
    for f in FILES:
        if not f.exists():
            print(f"跳过（不存在）：{f}")
            continue
        text = f.read_text(encoding="utf-8")
        new, notes = patch(text)
        if f.name == "index.html":
            pairs = [
                ("<title>学习总手册</title>", "<title>AI 架构学习系统：从机器学习到 DeepSeek</title>"),
                ('<span class="brand">学习总手册<span>点化学习系统 · 统一入口</span></span>',
                 '<span class="brand">AI 架构学习系统<span>从机器学习到 DeepSeek · 学习总手册</span></span>'),
                ("pre = '<h1>学习总手册</h1>'", "pre = '<h1>AI 架构学习系统</h1>'"),
                ("+ '<p>本学习系统把书点化为一套可跟着走的学习内容。",
                 "+ '<p>学习总手册：把书点化为一套可跟着走的学习内容。"),
            ]
            for a, b in pairs:
                if a in new:
                    new = new.replace(a, b)
                    notes.append(f"brand: {a[:24]}")
        if new != text:
            f.write_text(new, encoding="utf-8")
            print(f"✓ {f.name}: " + ", ".join(notes))
        else:
            print(f"- {f.name}: 无需改动")
    return 0


if __name__ == "__main__":
    sys.exit(main())
