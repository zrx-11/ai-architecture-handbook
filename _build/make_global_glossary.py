#!/usr/bin/env python3
"""汇总六本分册的术语表，生成跨书术语总表。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = [
    ("01-foundations", "基础篇：从零到 Transformer"),
    ("04-machine-learning", "机器学习基础：从任务到评估"),
    ("05-neural-networks", "神经网络：从一条直线推到反向传播"),
    ("06-deep-learning", "深度学习入门：从零手写神经网络"),
    ("02-paper-teardown", "论文拆解：R1 / V4 / V4.1"),
    ("03-architecture", "架构阐释：三代模型的设计逻辑"),
]


def main():
    lines = ["# 跨书术语总表", "",
             "按分册汇总，术语定义保留各书原有口径；同一术语在不同书里的差异，以对应章节为准。", ""]
    total = 0
    for d, label in BOOKS:
        mf = ROOT / d / "manifest.json"
        if not mf.exists():
            continue
        m = json.load(open(mf, encoding="utf-8"))
        gl = m.get("glossary", [])
        if not gl:
            continue
        total += len(gl)
        chap = {c["id"]: c.get("title", c["id"]) for c in m.get("chapters", [])}
        lines.append(f"## {label}（{len(gl)} 条）")
        lines.append("")
        lines.append("| 术语 | 白话定义 | 章节 |")
        lines.append("|---|---|---|")
        for g in gl:
            term = str(g.get("term", "")).replace("|", "\\|")
            definition = str(g.get("def", "")).replace("|", "\\|").replace("\n", " ")
            chapter = chap.get(g.get("chapterId"), g.get("chapterId", ""))
            lines.append(f"| {term} | {definition} | {chapter} |")
        lines.append("")

    lines += [
        "## 深潜课关键词",
        "",
        "| 术语 | 一句话解释 | 所在课程 |",
        "|---|---|---|",
        "| 词嵌入 | 把 token 编号映射成可训练的向量 | Transformer 深潜 第 2 节 |",
        "| 位置编码 | 给序列里的每个位置一个可区分信号，让注意力知道顺序 | Transformer 深潜 第 3 节 |",
        "| Q / K / V | 查询、键、值：用 Q 和 K 算相似度，再对 V 加权求和 | Transformer 深潜 第 4 节 |",
        "| 缩放点积注意力 | 点积除以 √d 后再 softmax，避免维度大时梯度饱和 | Transformer 深潜 第 4 节 |",
        "| 多头注意力 | 多组独立的 Q/K/V 并行，拼接后做线性变换 | Transformer 深潜 第 5 节 |",
        "| 掩码 | 阻止解码器看到未来 token 的注意力遮罩 | Transformer 深潜 第 9 节 |",
        "| 最大间隔 | 在所有能分开数据的超平面里，选离最近样本最远的那个 | SVM 深潜 第 1 节 |",
        "| 支持向量 | 决定间隔边界、对偶解里 α>0 的样本 | SVM 深潜 第 3–5 节 |",
        "| 对偶问题 | 把原问题转成只含样本内积的优化问题，便于用核 | SVM 深潜 第 3 节 |",
        "| KKT 条件 | 不等式约束下最优解必须满足的一组条件 | SVM 深潜 第 4 节 |",
        "| 松弛变量 | 软间隔里允许个别样本越界的变量 | SVM 深潜 第 6 节 |",
        "| hinge 损失 | max(0, 1 - y f(x))，错得越远惩罚越大 | SVM 深潜 第 6 节 |",
        "| 核技巧 | 用核函数直接算高维内积，避免显式映射 | SVM 深潜 第 8 节 |",
        "",
        f"合计 {total} 条分册术语，另有 13 条深潜课关键词。",
        "",
    ]
    out = ROOT / "00-跨书总览" / "术语总表.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ {out}（{total} 条分册术语）")


if __name__ == "__main__":
    main()
