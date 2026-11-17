#!/usr/bin/env python3
"""把已有学习项目拆成独立分册，合并进当前学习系统。

来源：
  _merge_sources/ai-ml-dl-rl-enlighten/02-机器学习   -> 04-machine-learning
  _merge_sources/neural-net-zero                     -> 05-neural-networks
  _merge_sources/ai-ml-dl-rl-enlighten/03-深度学习入门 -> 06-deep-learning
  _merge_sources/transformer/index.html              -> 07-transformer-deep/index.html
  _merge_sources/SVM/index.html                      -> 08-svm-deep/index.html

只复制到当前项目，不改动用户原仓库。
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_merge_sources"


def copy_book(src: Path, dst: Path, slug: str, title: str, subtitle: str, companion: str):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    # 清掉旧入口与旧伴侣，避免 build_handbook 误认
    for name in ["index.html", "交付说明.md"]:
        p = dst / name
        if p.exists():
            p.unlink()
    for p in dst.glob("*学习伴侣.html"):
        p.unlink()
    mf = dst / "manifest.json"
    m = json.load(open(mf, encoding="utf-8"))
    m["slug"] = slug
    m["title"] = title
    m["subtitle"] = subtitle
    m["companion"] = companion
    json.dump(m, open(mf, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✓ {dst.name}: {len(m.get('chapters', []))} 章 / {len(m.get('concepts', []))} 概念 / {len(m.get('quizzes', []))} 测验")


def copy_html(src: Path, dst_dir: Path):
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_dir / "index.html")
    print(f"✓ {dst_dir.name}: {src.stat().st_size/1024:.0f} KB")


def main():
    copy_book(SRC / "ai-ml-dl-rl-enlighten/02-机器学习", ROOT / "04-machine-learning",
              "machine-learning", "机器学习基础：从任务到评估",
              "周志华《机器学习》导读：16 章拆开算法、评估与术语",
              "machine-learning学习伴侣.html")
    copy_book(SRC / "neural-net-zero", ROOT / "05-neural-networks",
              "neural-networks", "神经网络：从一条直线推到反向传播",
              "从函数、导数、点积一路推到反向传播，不跳步",
              "neural-networks学习伴侣.html")
    copy_book(SRC / "ai-ml-dl-rl-enlighten/03-深度学习入门", ROOT / "06-deep-learning",
              "deep-learning-scratch", "深度学习入门：从零手写神经网络",
              "斋藤康毅《深度学习入门》导读：代码线与 CNN",
              "deep-learning学习伴侣.html")
    copy_html(SRC / "transformer/index.html", ROOT / "07-transformer-deep")
    copy_html(SRC / "SVM/index.html", ROOT / "08-svm-deep")


if __name__ == "__main__":
    main()
