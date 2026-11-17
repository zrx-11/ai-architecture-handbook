#!/usr/bin/env python3
"""给分册章节补深潜课与相邻分册的交叉链接。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LINKS = {
    "01-foundations/chapters/ch03-attention.md": (
        "\n## 想继续深入\n\n"
        "标准 Transformer 的位置编码、多头、掩码和训练目标，见 [Transformer 从零推导深潜课](../07-transformer-deep/index.html)。\n"
    ),
    "01-foundations/chapters/ch04-transformer-block.md": (
        "\n## 想继续深入\n\n"
        "把编码器/解码器、残差、层归一化和训练过程逐段推完，见 [Transformer 从零推导深潜课](../07-transformer-deep/index.html)。\n"
    ),
    "04-machine-learning/chapters/ch05.md": (
        "\n## 想继续深入\n\n"
        "神经网络的前向、损失、梯度和反向传播，见 [神经网络：从一条直线推到反向传播](../05-neural-networks/neural-networks学习伴侣.html)；"
        "代码实现见 [深度学习入门](../06-deep-learning/deep-learning学习伴侣.html)。\n"
    ),
    "04-machine-learning/chapters/ch06.md": (
        "\n## 想继续深入\n\n"
        "最大间隔、对偶、KKT、软间隔和核技巧的完整推导，见 [SVM 从零推导深潜课](../08-svm-deep/index.html)。\n"
    ),
}

for rel, note in LINKS.items():
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    marker = note.strip().splitlines()[0]
    if marker in text:
        print(f"- {rel}: 已有链接")
        continue
    p.write_text(text.rstrip() + "\n" + note, encoding="utf-8")
    print(f"✓ {rel}: 追加交叉链接")
