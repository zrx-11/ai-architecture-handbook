#!/usr/bin/env python3
"""本轮交付的端到端验证：7 步首页、09 分册、移动端/桌面端、搜索、测验。"""
import json, os, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
FAMILY = ROOT / "09-deepseek-family/deepseek-family学习伴侣.html"
results = []
def check(name, ok, extra=""):
    results.append({"check": name, "pass": bool(ok), "extra": extra})
    print(("PASS " if ok else "FAIL ") + name + (" | " + extra if extra else ""))

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/local/bin/chromium", args=["--no-sandbox","--disable-gpu"])
        page = browser.new_page(viewport={"width":1440,"height":900})
        errors=[]
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type=="error" and not re.search(r"mermaid|net::|ERR_", m.text or "") else None)
        page.goto("file://"+str(INDEX))
        page.wait_for_timeout(900)
        meta=page.evaluate("META")
        check("7 本书", len(meta)==7, str(len(meta)))
        check("首页 7 步", page.eval_on_selector_all(".step-card","els=>els.length")==7,
              str(page.eval_on_selector_all(".step-card","els=>els.length")))
        check("首页主线标题", "一条主线走完" in page.inner_text("#view"))
        check("资料库 13 项", page.eval_on_selector_all(".lib-item","els=>els.length")==13,
              str(page.eval_on_selector_all(".lib-item","els=>els.length")))
        # 每本书首末章 + 测验
        for m in meta:
            k=m["key"]; chs=page.evaluate(f"BOOKS['{k}'].manifest.chapters")
            check(f"{k} 章节数", len(chs)>0, str(len(chs)))
            for label,ch in (("首章",chs[0]["id"]),("末章",chs[-1]["id"])):
                page.evaluate(f"location.hash='#/book/{k}/chapter/{ch}'"); page.wait_for_timeout(450)
                check(f"{k} {label}", len(page.inner_text("#view"))>300, f"{len(page.inner_text('#view'))} 字")
            page.evaluate(f"location.hash='#/book/{k}/quiz/all'"); page.wait_for_timeout(450)
            n=page.eval_on_selector_all(".quiz-item","els=>els.length")
            check(f"{k} 测验", n>0, f"{n} 题")
            if n:
                info=page.evaluate("""()=>{const el=document.querySelector('.quiz-item');const q=(BOOKS[cur.book].manifest.quizzes||[]).find(x=>x.id===el.dataset.qid);return q?{qid:q.id,type:q.type,answer:q.answer}:null}""")
                sel=f".quiz-item[data-qid='{info['qid']}']"
                if info['type']=='single': page.click(f"{sel} input[value='{info['answer']}']")
                elif info['type']=='multi':
                    for a in info['answer']: page.click(f"{sel} input[value='{a}']")
                else: page.fill(f"{sel} .quiz-blank", str(info['answer']))
                page.click(f"{sel} .quiz-check"); page.wait_for_timeout(250)
                check(f"{k} 作答反馈", "正确" in page.inner_text(f"{sel} .quiz-feedback"))
        # 09 关键页
        for pageId, needle in [("chapter/ch01","家族地图"),("chapter/ch04","MLA"),("chapter/ch09","890"),("chapter/ch11","选型"),("chapter/ch13","671B"),("chapter/ch14","config.json"),("concept/c04","多头潜在注意力"),("concept/c11","CED")]:
            page.evaluate(f"location.hash='#/book/deepseek-family/{pageId}'"); page.wait_for_timeout(450)
            txt=page.inner_text("#view")
            check(f"09 {pageId}", needle in txt, f"{len(txt)} 字")
        page.evaluate("location.hash='#/book/deepseek-family/cards'"); page.wait_for_timeout(450)
        check("09 抽认卡", page.eval_on_selector_all(".flashcard","els=>els.length")>=1)
        page.evaluate("location.hash='#/book/deepseek-family/glossary'"); page.wait_for_timeout(450)
        check("09 术语表 68", page.eval_on_selector_all("#glossary-list li","els=>els.length")==68,
              str(page.eval_on_selector_all("#glossary-list li","els=>els.length")))
        page.evaluate("location.hash='#/book/deepseek-family/diagnosis'"); page.wait_for_timeout(450)
        check("09 诊断页", "诊断" in page.inner_text("#view"))
        # 搜索
        page.evaluate("location.hash='#/cross/doc1'"); page.wait_for_timeout(400)
        page.fill("#q","MLA"); page.wait_for_timeout(500)
        hits=page.eval_on_selector_all(".search-hit","els=>els.length")
        check("搜索 MLA", hits>0, f"{hits} 条")
        # 桌面布局
        box=page.eval_on_selector(".main","el=>{const r=el.getBoundingClientRect();return [r.left,r.right,r.width]}")
        check("桌面主栏宽度", box[2]<=940 and box[0]>=100, str(box))
        # 移动端
        page.set_viewport_size({"width":390,"height":844})
        page.evaluate("location.hash='#/book/deepseek-family/chapter/ch09'"); page.wait_for_timeout(500)
        m=page.eval_on_selector(".main","el=>{const r=el.getBoundingClientRect();return [r.left,r.right,el.scrollWidth]}")
        check("移动端无横向溢出", m[1]<=392 and m[2]<=390, str(m))
        nav=page.eval_on_selector("#nav","el=>getComputedStyle(el).maxHeight") if page.query_selector("#nav") else "none"
        check("移动端导航限高", nav in ("46vh","none") or "px" in nav, nav)
        # 09 独立伴侣
        page2=browser.new_page(viewport={"width":1440,"height":900})
        page2.goto("file://"+str(FAMILY)); page2.wait_for_timeout(700)
        txt=page2.inner_text("body")
        check("09 伴侣打开", "家族地图" in txt and "105+ 张模型卡" in txt)
        check("09 伴侣 14 章", page2.evaluate("DATA.manifest.chapters.length")==14, str(page2.evaluate("DATA.manifest.chapters.length")))
        page2.evaluate("location.hash='#/quiz/all'"); page2.wait_for_timeout(600)
        check("09 伴侣测验 42", page2.eval_on_selector_all(".quiz-item","els=>els.length")==42, str(page2.eval_on_selector_all(".quiz-item","els=>els.length")))
        page2.evaluate("location.hash='#/chapter/ch04'"); page2.wait_for_timeout(2500)
        check("09 伴侣 KaTeX", page2.eval_on_selector_all(".katex","els=>els.length")>=10, str(page2.eval_on_selector_all(".katex","els=>els.length")))
        check("09 伴侣 Mermaid", page2.eval_on_selector_all(".mermaid svg","els=>els.length")>=1, str(page2.eval_on_selector_all(".mermaid svg","els=>els.length")))
        check("控制台无错误", len(errors)==0, " || ".join(errors[:3]))
        browser.close()
    ok=sum(1 for r in results if r["pass"])
    print(f"\n=== {ok}/{len(results)} 通过 ===")
    json.dump(results, open(ROOT/"_build/verify_round1.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    return 0 if ok==len(results) else 1

if __name__=="__main__":
    sys.exit(main())
