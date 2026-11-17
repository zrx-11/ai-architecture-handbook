#!/usr/bin/env python3
"""生成三本书的 manifest.json 与配套 Markdown（quiz / flashcards / glossary / patterns / cheatsheet / paths）。"""
import json, os, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOKS = []

# ============================ Book 1 ============================
BOOKS.append({
 "slug": "deepseek-foundations",
 "title": "基础篇：从零到 Transformer",
 "subtitle": "读懂 DeepSeek 论文之前，先把数字、注意力与 V3 地基补齐",
 "book": {"title": "基础篇：从零到 Transformer", "author": "本课程整理", "source": [
     "DeepSeek-V3 技术报告（arXiv:2412.19437）",
     "DeepSeek-R1 论文（arXiv:2501.12948）",
     "DeepSeek-V4 技术报告（arXiv:2606.19348）"]},
 "audience": "数学与代码接近零基础",
 "goal": "能读懂 Transformer 与 DeepSeek-V3 的架构图，为读 R1/V4/V4.1 论文打底",
 "dir": "01-foundations",
 "learningPath": [
   {"step":"01","title":"向量、矩阵、softmax","chapterIds":["ch01"],"checkpoint":"完成 ch01 自测，能手算矩阵乘向量与 softmax"},
   {"step":"02","title":"参数、损失、梯度","chapterIds":["ch02"],"checkpoint":"完成 ch02 自测，能算一次梯度更新"},
   {"step":"03","title":"注意力机制","chapterIds":["ch03"],"checkpoint":"能手算 3 个 token 的注意力权重"},
   {"step":"04","title":"Transformer 一层楼","chapterIds":["ch04"],"checkpoint":"能画出一次前向的 shape 变化"},
   {"step":"05","title":"V3 的三块地基","chapterIds":["ch05"],"checkpoint":"能说出 MLA、MoE、MTP 各解决什么问题"},
   {"step":"06","title":"附录：形状、公式与手算","chapterIds":["ch06"],"checkpoint":"能手算注意力、梯度与 KV cache 字节"},
 ],
 "chapters": [
   {"id":"ch01","title":"第 1 章：数字怎么变成“意思”：向量、矩阵与 softmax","file":"chapters/ch01-vectors-matrices-softmax.md","difficulty":1,"source":"本课程整理 · 基础数学","prerequisites":[]},
   {"id":"ch02","title":"第 2 章：模型怎么学会：参数、损失、梯度","file":"chapters/ch02-learning-parameters.md","difficulty":1,"source":"本课程整理 · 训练基础","prerequisites":["ch01"]},
   {"id":"ch03","title":"第 3 章：注意力机制：一句话里谁该看谁","file":"chapters/ch03-attention.md","difficulty":2,"source":"本课程整理 · 注意力机制","prerequisites":["ch01","ch02"]},
   {"id":"ch04","title":"第 4 章：Transformer 一层一层拆","file":"chapters/ch04-transformer-block.md","difficulty":2,"source":"本课程整理 · Transformer","prerequisites":["ch03"]},
   {"id":"ch05","title":"第 5 章：DeepSeek-V3 的三块地基","file":"chapters/ch05-v3-foundations.md","difficulty":3,"source":"DeepSeek-V3 技术报告（arXiv:2412.19437）§2","prerequisites":["ch03","ch04"]},
   {"id":"ch06","title":"附录：形状、公式与手算清单","file":"chapters/ch06-shapes-formulas.md","difficulty":2,"source":"本课程整理 · 手算附录","prerequisites":["ch05"]},
 ],
 "concepts": [
   {"id":"c01","title":"向量","file":"concepts/c01-vector.md","chapterIds":["ch01"],"difficulty":"基础","source":"本课程整理 · 基础数学","prerequisites":[]},
   {"id":"c02","title":"矩阵乘法","file":"concepts/c02-matrix-multiplication.md","chapterIds":["ch01"],"difficulty":"基础","source":"本课程整理 · 基础数学","prerequisites":["c01"]},
   {"id":"c03","title":"softmax","file":"concepts/c03-softmax.md","chapterIds":["ch01"],"difficulty":"基础","source":"本课程整理 · 基础数学","prerequisites":["c01"]},
   {"id":"c04","title":"参数与损失","file":"concepts/c04-parameters-loss.md","chapterIds":["ch02"],"difficulty":"基础","source":"本课程整理 · 训练基础","prerequisites":["c02"]},
   {"id":"c05","title":"梯度下降","file":"concepts/c05-gradient-descent.md","chapterIds":["ch02"],"difficulty":"基础","source":"本课程整理 · 训练基础","prerequisites":["c04"]},
   {"id":"c06","title":"注意力","file":"concepts/c06-attention.md","chapterIds":["ch03","ch04"],"difficulty":"进阶","source":"本课程整理 · 注意力","prerequisites":["c02","c03"]},
   {"id":"c07","title":"Q / K / V","file":"concepts/c07-qkv.md","chapterIds":["ch03","ch05"],"difficulty":"进阶","source":"本课程整理 · 注意力","prerequisites":["c06"],"depthFragment":"concepts/c07-qkv-depth.md"},
   {"id":"c08","title":"残差连接","file":"concepts/c08-residual.md","chapterIds":["ch04"],"difficulty":"基础","source":"本课程整理 · Transformer","prerequisites":["c02"]},
   {"id":"c09","title":"RMSNorm","file":"concepts/c09-rmsnorm.md","chapterIds":["ch04"],"difficulty":"进阶","source":"本课程整理 · Transformer","prerequisites":["c01","c08"]},
   {"id":"c10","title":"前馈网络（FFN）","file":"concepts/c10-ffn.md","chapterIds":["ch04","ch05"],"difficulty":"进阶","source":"本课程整理 · Transformer","prerequisites":["c02","c09"]},
   {"id":"c11","title":"自回归生成","file":"concepts/c11-autoregressive.md","chapterIds":["ch04"],"difficulty":"基础","source":"本课程整理 · 生成","prerequisites":["c03","c04"]},
   {"id":"c12","title":"MLA（多头潜在注意力）","file":"concepts/c12-mla.md","chapterIds":["ch05"],"difficulty":"高难","source":"DeepSeek-V3 技术报告 §2.1","prerequisites":["c07","c16"],"depthFragment":"concepts/c12-mla-depth.md"},
   {"id":"c13","title":"DeepSeekMoE","file":"concepts/c13-deepseekmoe.md","chapterIds":["ch05"],"difficulty":"高难","source":"DeepSeek-V3 技术报告 §2.2","prerequisites":["c03","c10"],"depthFragment":"concepts/c13-moe-depth.md"},
   {"id":"c14","title":"MTP（多 token 预测）","file":"concepts/c14-mtp.md","chapterIds":["ch05"],"difficulty":"进阶","source":"DeepSeek-V3 技术报告 §2.3","prerequisites":["c11"]},
   {"id":"c15","title":"负载均衡","file":"concepts/c15-load-balancing.md","chapterIds":["ch05"],"difficulty":"进阶","source":"DeepSeek-V3 技术报告 §2.2","prerequisites":["c03","c13"]},
   {"id":"c16","title":"KV cache","file":"concepts/c16-kv-cache.md","chapterIds":["ch05"],"difficulty":"进阶","source":"DeepSeek-V3 技术报告 §2.1","prerequisites":["c07","c11"]},
 ],
 "glossary": [
   {"term":"向量","def":"一串有顺序的数字，长度叫维度。","chapterId":"ch01"},
   {"term":"矩阵乘法","def":"左矩阵每行与右矩阵每列做点积，得到新矩阵。","chapterId":"ch01"},
   {"term":"softmax","def":"把分数转成非负、总和为 1 的权重。","chapterId":"ch01"},
   {"term":"token","def":"模型处理文本的基本单位，可以是一个字、一个词或词的一部分。","chapterId":"ch01"},
   {"term":"embedding","def":"把 token 编号映射成固定长度向量的表。","chapterId":"ch01"},
   {"term":"参数","def":"模型里可训练的数值，比如矩阵元素。","chapterId":"ch02"},
   {"term":"损失","def":"衡量预测与正确答案差距的标量。","chapterId":"ch02"},
   {"term":"梯度","def":"损失对参数的变化率，指示更新方向。","chapterId":"ch02"},
   {"term":"学习率","def":"每次参数更新走多大的一步。","chapterId":"ch02"},
   {"term":"过拟合","def":"训练集上损失很小，换数据就变差。","chapterId":"ch02"},
   {"term":"注意力","def":"按 token 间相似度加权收集信息的机制。","chapterId":"ch03"},
   {"term":"Q / K / V","def":"查询、键、值，同一输入的三次投影。","chapterId":"ch03"},
   {"term":"多头注意力","def":"并行多套 Q/K/V，捕捉不同关系。","chapterId":"ch03"},
   {"term":"因果掩码","def":"禁止每个 token 看到未来 token。","chapterId":"ch03"},
   {"term":"残差连接","def":"把子层输入加到子层输出。","chapterId":"ch04"},
   {"term":"RMSNorm","def":"用均方根缩放向量的归一化。","chapterId":"ch04"},
   {"term":"FFN","def":"对每个 token 独立做升维-激活-降维。","chapterId":"ch04"},
   {"term":"自回归生成","def":"逐个预测下一个 token 并接回输入。","chapterId":"ch04"},
   {"term":"MLA","def":"用低维潜向量压缩 KV cache 的注意力。","chapterId":"ch05"},
   {"term":"DeepSeekMoE","def":"共享专家 + 细粒度路由专家的混合专家结构。","chapterId":"ch05"},
   {"term":"MTP","def":"训练时额外预测未来第 2 个 token。","chapterId":"ch05"},
   {"term":"KV cache","def":"推理时缓存历史 token 的 K/V。","chapterId":"ch05"},
   {"term":"专家塌缩","def":"MoE 路由总选少数专家，其他专家学不到东西。","chapterId":"ch05"},
 ],
 "quizzes": [
   {"id":"q01","chapterId":"ch01","type":"single","question":"一个 2×3 矩阵乘一个 3 维向量，结果是什么形状？","options":["2×3 矩阵","3 维向量","2 维向量","一个标量"],"answer":2,"explain":"左矩阵两行，每行与 3 维向量做一次加权求和，得到两个数。","relatedConceptId":"c02"},
   {"id":"q02","chapterId":"ch01","type":"single","question":"对分数 [0, 0, 0] 做 softmax，输出是什么？","options":["[0, 0, 0]","[1/3, 1/3, 1/3]","[1, 0, 0]","[3, 3, 3]"],"answer":1,"explain":"三个 e^0=1，总和 3，各占三分之一。","relatedConceptId":"c03"},
   {"id":"q03","chapterId":"ch01","type":"single","question":"embedding 表在模型里做什么？","options":["把 token 编号映射成向量","把向量压缩成标量","把句子翻译成英文","计算损失"],"answer":0,"explain":"embedding 表按 token 编号查出一串固定长度的向量。","relatedConceptId":"c01"},
   {"id":"q04","chapterId":"ch02","type":"single","question":"梯度为正时，梯度下降会把参数往哪个方向更新？","options":["增大","减小","不变","随机"],"answer":1,"explain":"更新规则是减去学习率乘梯度，梯度为正就减小参数。","relatedConceptId":"c05"},
   {"id":"q05","chapterId":"ch02","type":"single","question":"w=1、x=2、y=3，损失 L=(wx-y)^2，对 w 的梯度是多少？","options":["-4","4","-2","2"],"answer":0,"explain":"2(wx-y)x = 2(2-3)×2 = -4。","relatedConceptId":"c05"},
   {"id":"q06","chapterId":"ch02","type":"single","question":"学习率取得过大，训练曲线通常会出现什么？","options":["收敛更快且稳定","损失震荡或发散","参数不再更新","模型自动变小"],"answer":1,"explain":"步子太大会跨过谷底，损失震荡甚至变成 NaN。","relatedConceptId":"c04"},
   {"id":"q07","chapterId":"ch03","type":"single","question":"注意力里真正被加权混合的是哪一项？","options":["Query","Key","Value","因果掩码"],"answer":2,"explain":"Q 和 K 只用于算分数，输出是 V 的加权和。","relatedConceptId":"c06"},
   {"id":"q08","chapterId":"ch03","type":"single","question":"分数 [1, 1, 1] 经过 softmax 后的权重是什么？","options":["[1, 0, 0]","[1/3, 1/3, 1/3]","[0.5, 0.5, 0]","[3, 3, 3]"],"answer":1,"explain":"三个 e^1 相等，各占三分之一。","relatedConceptId":"c03"},
   {"id":"q09","chapterId":"ch03","type":"single","question":"注意力分数为什么要除以 sqrt(d_k)？","options":["让分数更大","防止 softmax 过度集中","增加注意力头数","去掉位置信息"],"answer":1,"explain":"维度高时点积数值大，softmax 会过度集中，梯度变小。","relatedConceptId":"c06"},
   {"id":"q10","chapterId":"ch04","type":"single","question":"一个 Transformer 层里，残差连接加在哪两处？","options":["只在注意力后","只在 FFN 后","注意力和 FFN 后各一次","每层最后只加一次"],"answer":2,"explain":"注意力和 FFN 是两个子层，各自带残差。","relatedConceptId":"c08"},
   {"id":"q11","chapterId":"ch04","type":"single","question":"输入形状 [6, 16] 经过 4 倍 FFN 后，中间层形状是什么？","options":["[6, 16]","[6, 64]","[24, 16]","[6, 4]"],"answer":1,"explain":"隐藏维度 16 放大 4 倍是 64，token 数不变。","relatedConceptId":"c10"},
   {"id":"q12","chapterId":"ch04","type":"single","question":"为什么位置信息必须显式注入 Transformer？","options":["让模型知道词序","减少参数量","加速训练","替代注意力"],"answer":0,"explain":"查表得到的 token 向量不含顺序信息，不注入位置就分不清词序。","relatedConceptId":"c11"},
   {"id":"q13","chapterId":"ch05","type":"single","question":"MLA 推理时缓存的核心内容是什么？","options":["每个头的完整 K 和 V","低维潜向量和 RoPE key","只有 Query","整个隐藏层输出"],"answer":1,"explain":"MLA 缓存压缩后的 c_KV 和承载位置的 RoPE key。","relatedConceptId":"c12"},
   {"id":"q14","chapterId":"ch05","type":"single","question":"DeepSeekMoE 中共享专家的作用是什么？","options":["只处理英文","始终激活，兜住通用知识","只处理数学题","替代注意力"],"answer":1,"explain":"共享专家对所有 token 生效，减少路由专家重复学习通用知识。","relatedConceptId":"c13"},
   {"id":"q15","chapterId":"ch05","type":"single","question":"MTP 在训练时额外预测哪个位置？","options":["只预测 t+1","额外预测 t+2","预测前一个 token","随机位置"],"answer":1,"explain":"在位置 t 额外预测 t+2，增加训练信号密度。","relatedConceptId":"c14"},
 ],
 "flashcards": [
   {"id":"f01","chapterId":"ch01","front":"向量在模型里是什么？","back":"一串有顺序的数字，长度叫维度。","tags":["基础","向量"]},
   {"id":"f02","chapterId":"ch01","front":"矩阵乘法的计算规则？","back":"左矩阵每一行与右矩阵每一列做点积。","tags":["基础","矩阵"]},
   {"id":"f03","chapterId":"ch01","front":"softmax 的两个关键性质？","back":"输出非负、总和为 1，并且保持原有大小顺序。","tags":["基础","softmax"]},
   {"id":"f04","chapterId":"ch01","front":"embedding 表做什么？","back":"把 token 编号映射成固定长度的向量。","tags":["基础","embedding"]},
   {"id":"f05","chapterId":"ch02","front":"参数、损失、梯度各是什么？","back":"参数是可调旋钮，损失是差距分数，梯度是损失对参数的变化率。","tags":["训练","基础"]},
   {"id":"f06","chapterId":"ch02","front":"梯度下降的更新公式？","back":"w ← w - η·∂L/∂w。","tags":["训练","梯度"]},
   {"id":"f07","chapterId":"ch02","front":"学习率过大和过小分别会怎样？","back":"过大震荡或发散，过小学得慢。","tags":["训练","学习率"]},
   {"id":"f08","chapterId":"ch02","front":"过拟合是什么？","back":"训练集损失很小，换一批数据表现变差。","tags":["训练","泛化"]},
   {"id":"f09","chapterId":"ch03","front":"Q、K、V 各自负责什么？","back":"Q 找信息，K 提供标签，V 提供实际内容。","tags":["注意力","QKV"]},
   {"id":"f10","chapterId":"ch03","front":"注意力分数怎么算？","back":"Q 与 K 点积，除以 sqrt(d_k)，再 softmax。","tags":["注意力","公式"]},
   {"id":"f11","chapterId":"ch03","front":"为什么要除以 sqrt(d_k)？","back":"防止高维点积过大，softmax 过度集中导致梯度消失。","tags":["注意力","缩放"]},
   {"id":"f12","chapterId":"ch03","front":"因果掩码的作用？","back":"把未来位置的分数设为负无穷，禁止模型偷看答案。","tags":["注意力","掩码"]},
   {"id":"f13","chapterId":"ch04","front":"Transformer 一层有哪两段？","back":"多头注意力和前馈网络，各自带残差与归一化。","tags":["Transformer","结构"]},
   {"id":"f14","chapterId":"ch04","front":"残差连接的公式？","back":"y = x + Layer(x)。","tags":["Transformer","残差"]},
   {"id":"f15","chapterId":"ch04","front":"RMSNorm 与 LayerNorm 的区别？","back":"RMSNorm 不减均值，只除以均方根，计算更快。","tags":["Transformer","归一化"]},
   {"id":"f16","chapterId":"ch04","front":"FFN 的形状怎么变？","back":"先升到约 4 倍中间维度，激活后再降回隐藏维度。","tags":["Transformer","FFN"]},
   {"id":"f17","chapterId":"ch05","front":"MLA 缓存什么？","back":"低维潜向量 c_KV 和解耦的 RoPE key。","tags":["DeepSeek","MLA"]},
   {"id":"f18","chapterId":"ch05","front":"DeepSeekMoE 的结构？","back":"1 个共享专家 + 多个细粒度路由专家，每 token 激活 top-k 个路由专家。","tags":["DeepSeek","MoE"]},
   {"id":"f19","chapterId":"ch05","front":"MTP 的训练目标？","back":"在每个位置额外预测未来第 2 个 token。","tags":["DeepSeek","MTP"]},
   {"id":"f20","chapterId":"ch05","front":"无辅助损失负载均衡怎么做？","back":"给每个专家一个可学习偏置，按负载调偏置，不往主损失加辅助项。","tags":["DeepSeek","负载均衡"]},
 ],
 "patterns": """# 模式与框架库

## 框架：从数字到结构
学任何一个模型结构，按“输入是什么数字 → 做哪种运算 → 形状怎么变 → 解决什么问题”四步走。不要先背名字。

## 框架：三件套理解法
每个抽象概念至少配一个类比、一个图示、一个可手算的实例；缺一个就容易停在“好像懂了”。

## 决策规则
- 看到公式先问“每个符号是什么”，再问“为什么这样设计”。
- 看到架构先问“它省的是计算、显存还是带宽”。
- 看到数字先问“单位是什么、和谁比”。

## 反模式
- 只背缩写，不追动机。
- 把“注意力权重”当成模型解释。
- 把总参数和激活参数混为一谈。
""",
 "cheatsheet": """# 速查表

## 公式与规则
| 场景 | 内容 |
|---|---|
| 矩阵乘向量 | 每行与向量做点积 |
| softmax | $e^{z_i}/\\sum_j e^{z_j}$ |
| 梯度下降 | $w\\leftarrow w-\\eta\\partial L/\\partial w$ |
| 注意力分数 | $q\\cdot k/\\sqrt{d_k}$ |
| 注意力输出 | $\\sum_j\\alpha_{ij}v_j$ |
| 残差 | $y=x+\\mathrm{Layer}(x)$ |
| RMSNorm | $x/\\sqrt{\\mathrm{mean}(x^2)+\\epsilon}\\odot g$ |

## 关键数字
| 项目 | 数值 |
|---|---|
| V3 总参数 / 激活 | 671B / 37B |
| V3 层数 / 头数 | 61 / 128 |
| V3 路由专家 / 激活 | 256 / 8 |
| V3 预训练 token | 14.8T |
| V3 上下文 | 128K |
""",
})

# ============================ Book 2 ============================
BOOKS.append({
 "slug": "deepseek-papers",
 "title": "论文拆解：R1 / V4 / V4.1",
 "subtitle": "按“问题—方法—数据—实验—局限”逐篇拆三篇 DeepSeek 论文",
 "book": {"title": "论文拆解：R1 / V4 / V4.1", "author": "本课程整理", "source": [
     "DeepSeek-R1（arXiv:2501.12948）",
     "DeepSeek-V4（arXiv:2606.19348）",
     "DeepSeek-V4.1-Flash（arXiv:2609.19969）"]},
 "audience": "读完基础篇、准备读原论文的读者",
 "goal": "能独立拆解三篇论文的问题、方法、实验与局限，并判断结论的边界",
 "dir": "02-paper-teardown",
 "learningPath": [
   {"step":"01","title":"R1 上：问题、R1-Zero、GRPO","chapterIds":["ch06"],"checkpoint":"能复述 GRPO 的采样、奖励、优势计算"},
   {"step":"02","title":"R1 下：四阶段与蒸馏","chapterIds":["ch07"],"checkpoint":"能画出 R1 完整训练流程并说出局限"},
   {"step":"03","title":"V4：CSA/HCA、mHC、Muon","chapterIds":["ch08"],"checkpoint":"能说出 1M 上下文省的是哪两项成本"},
   {"step":"04","title":"V4.1：CED、CSA2、Engram、DSpark","chapterIds":["ch09"],"checkpoint":"能解释 prefill 8B 与 decode 16B 的来源"},
   {"step":"05","title":"附录：论文公式逐项拆解","chapterIds":["ch10"],"checkpoint":"能复算 GRPO、CSA、mHC 与 KV 字节"},
 ],
 "chapters": [
   {"id":"ch06","title":"第 6 章：R1 论文拆解（上）：先学会读论文，再看 R1-Zero","file":"chapters/ch06-r1-part1.md","difficulty":2,"source":"DeepSeek-R1 论文（arXiv:2501.12948）§1–§3","prerequisites":[]},
   {"id":"ch07","title":"第 7 章：R1 论文拆解（下）：四阶段流水线、蒸馏与局限","file":"chapters/ch07-r1-part2.md","difficulty":3,"source":"DeepSeek-R1 论文 §2–§4、§6","prerequisites":["ch06"]},
   {"id":"ch08","title":"第 8 章：V4 论文拆解：百万上下文的成本怎么砍","file":"chapters/ch08-v4.md","difficulty":3,"source":"DeepSeek-V4 技术报告（arXiv:2606.19348）§2–§5","prerequisites":["ch07"]},
   {"id":"ch09","title":"第 9 章：V4.1 论文拆解：非对称 CED 与 KV cache 极限","file":"chapters/ch09-v41.md","difficulty":3,"source":"DeepSeek-V4.1-Flash 论文（arXiv:2609.19969）§2–§5","prerequisites":["ch08"]},
   {"id":"ch10","title":"附录：论文公式逐项拆解","file":"chapters/ch10-formulas.md","difficulty":3,"source":"本课程整理 · 公式附录","prerequisites":["ch09"]},
 ],
 "concepts": [
   {"id":"c17","title":"GRPO（组相对策略优化）","file":"concepts/c17-grpo.md","chapterIds":["ch06"],"difficulty":"高难","source":"DeepSeek-R1 论文 §2.2","prerequisites":[],"depthFragment":"concepts/c17-grpo-depth.md"},
   {"id":"c18","title":"规则奖励","file":"concepts/c18-rule-reward.md","chapterIds":["ch06","ch07"],"difficulty":"进阶","source":"DeepSeek-R1 论文 §2.2","prerequisites":["c17"]},
   {"id":"c19","title":"冷启动","file":"concepts/c19-cold-start.md","chapterIds":["ch07"],"difficulty":"基础","source":"DeepSeek-R1 论文 §2.3.1","prerequisites":[]},
   {"id":"c20","title":"拒绝采样","file":"concepts/c20-rejection-sampling.md","chapterIds":["ch07"],"difficulty":"进阶","source":"DeepSeek-R1 论文 §2.3.2","prerequisites":["c17","c19"]},
   {"id":"c21","title":"知识蒸馏","file":"concepts/c21-distillation.md","chapterIds":["ch07"],"difficulty":"进阶","source":"DeepSeek-R1 论文 §2.3.3","prerequisites":["c20"]},
   {"id":"c22","title":"CSA（压缩稀疏注意力）","file":"concepts/c22-csa.md","chapterIds":["ch08"],"difficulty":"高难","source":"DeepSeek-V4 技术报告 §2.3.1","prerequisites":[],"depthFragment":"concepts/c22-csa-depth.md"},
   {"id":"c23","title":"HCA（重度压缩注意力）","file":"concepts/c23-hca.md","chapterIds":["ch08"],"difficulty":"高难","source":"DeepSeek-V4 技术报告 §2.3.2","prerequisites":["c22"]},
   {"id":"c24","title":"mHC（流形约束超连接）","file":"concepts/c24-mhc.md","chapterIds":["ch08","ch09"],"difficulty":"高难","source":"DeepSeek-V4 技术报告 §2.2","prerequisites":[],"depthFragment":"concepts/c24-mhc-depth.md"},
   {"id":"c25","title":"Muon 优化器","file":"concepts/c25-muon.md","chapterIds":["ch08"],"difficulty":"高难","source":"DeepSeek-V4 技术报告 §2.4","prerequisites":[]},
   {"id":"c26","title":"CED（因果编码器—解码器）","file":"concepts/c26-ced.md","chapterIds":["ch09"],"difficulty":"高难","source":"DeepSeek-V4.1-Flash 论文 §2.2","prerequisites":["c28"],"depthFragment":"concepts/c26-ced-depth.md"},
   {"id":"c27","title":"CSA2（压缩稀疏注意力 2）","file":"concepts/c27-csa2.md","chapterIds":["ch09"],"difficulty":"高难","source":"DeepSeek-V4.1-Flash 论文 §2.3","prerequisites":["c22","c23","c26"],"depthFragment":"concepts/c27-csa2-depth.md"},
   {"id":"c28","title":"SWA（滑动窗口注意力）","file":"concepts/c28-swa.md","chapterIds":["ch08","ch09"],"difficulty":"进阶","source":"DeepSeek-V4/V4.1 技术报告","prerequisites":[]},
   {"id":"c29","title":"Engram（条件记忆）","file":"concepts/c29-engram.md","chapterIds":["ch09"],"difficulty":"进阶","source":"DeepSeek-V4.1-Flash 论文 §2.4.2","prerequisites":[]},
   {"id":"c30","title":"DSpark（投机解码）","file":"concepts/c30-dspark.md","chapterIds":["ch09"],"difficulty":"进阶","source":"DeepSeek-V4.1-Flash 论文 §2.4.3","prerequisites":["c28"]},
   {"id":"c31","title":"FP4 量化","file":"concepts/c31-fp4.md","chapterIds":["ch09"],"difficulty":"进阶","source":"DeepSeek-V4/V4.1 技术报告","prerequisites":[]},
 ],
 "glossary": [
   {"term":"R1-Zero","def":"V3-Base 直接做纯 RL、不做冷启动得到的推理模型。","chapterId":"ch06"},
   {"term":"GRPO","def":"用组内相对优势替代价值模型的策略优化算法。","chapterId":"ch06"},
   {"term":"规则奖励","def":"用确定性规则判分，如答案匹配、格式检查。","chapterId":"ch06"},
   {"term":"冷启动","def":"RL 前用少量高质量长链推理做 SFT，稳定格式。","chapterId":"ch07"},
   {"term":"拒绝采样","def":"生成多个回答，只保留达标样本做 SFT。","chapterId":"ch07"},
   {"term":"知识蒸馏","def":"让学生模型学习教师模型的输出。","chapterId":"ch07"},
   {"term":"奖励黑客","def":"模型钻奖励漏洞拿高分但没真完成任务。","chapterId":"ch07"},
   {"term":"过程奖励模型（PRM）","def":"给推理每一步打分的奖励模型，R1 尝试后未作主方案。","chapterId":"ch07"},
   {"term":"MCTS","def":"蒙特卡洛树搜索，R1 尝试后未作主方案。","chapterId":"ch07"},
   {"term":"CSA","def":"每 4 个 token 压 1 条再做 top-k 稀疏的注意力。","chapterId":"ch08"},
   {"term":"HCA","def":"每 128 个 token 压 1 条再做稠密注意力的注意力。","chapterId":"ch08"},
   {"term":"mHC","def":"用双随机矩阵混合多条残差流的超连接。","chapterId":"ch08"},
   {"term":"Muon","def":"对梯度矩阵做正交化的优化器。","chapterId":"ch08"},
   {"term":"Sinkhorn-Knopp","def":"交替行列归一化，把矩阵投影到双随机流形。","chapterId":"ch08"},
   {"term":"双随机矩阵","def":"行和、列和都为 1 的非负矩阵。","chapterId":"ch08"},
   {"term":"CED","def":"前半编码器、后半解码器，解码全局 KV 由编码器末端投影。","chapterId":"ch09"},
   {"term":"CSA2","def":"CSA 的跨层复用版本，有 Full/Reindex/Reuse 三模式。","chapterId":"ch09"},
   {"term":"SWA","def":"只看最近固定窗口的滑动窗口注意力。","chapterId":"ch09"},
   {"term":"SWA Bounded Replay","def":"只回放最近一个窗口重建 SWA 缓存。","chapterId":"ch09"},
   {"term":"Engram","def":"用哈希查表的条件记忆模块。","chapterId":"ch09"},
   {"term":"DSpark","def":"V4.1 独立训练的投机解码 drafter。","chapterId":"ch09"},
   {"term":"FP4","def":"4 位浮点量化，存储和带宽约为 FP16 的 1/4。","chapterId":"ch09"},
   {"term":"全局 KV cache","def":"常驻 HBM 的主 KV 缓存；V4.1 为 890 B/token。","chapterId":"ch09"},
   {"term":"持久 KV cache","def":"放 SSD/主机内存、用于前缀复用的缓存。","chapterId":"ch09"},
   {"term":"预填充（prefill）","def":"一次性读入整段输入并建立 KV cache。","chapterId":"ch09"},
   {"term":"解码（decode）","def":"逐 token 生成输出。","chapterId":"ch09"},
 ],
 "quizzes": [
   {"id":"q01","chapterId":"ch06","type":"single","question":"R1-Zero 的奖励由哪两部分组成？","options":["过程奖励 + 结果奖励","准确性奖励 + 格式奖励","人类偏好 + 长度惩罚","价值模型 + 策略模型"],"answer":1,"explain":"论文明确只用规则化的准确性奖励和格式奖励。","relatedConceptId":"c18"},
   {"id":"q02","chapterId":"ch06","type":"blank","question":"GRPO 中优势的分母是组内______。","answer":"标准差","explain":"优势 =（奖励 - 组内均值）/ 组内标准差。","relatedConceptId":"c17"},
   {"id":"q03","chapterId":"ch06","type":"single","question":"R1-Zero 的初始基座是哪个模型？","options":["DeepSeek-V3-Base","DeepSeek-V4-Flash","Qwen-7B","Llama-70B"],"answer":0,"explain":"R1-Zero 从 V3-Base 出发做纯 RL。","relatedConceptId":"c17"},
   {"id":"q04","chapterId":"ch07","type":"single","question":"R1 的冷启动数据规模大约是多少？","options":["几千条","80 万条","8 万条","45T token"],"answer":0,"explain":"冷启动是几千条人工高质量长链推理。","relatedConceptId":"c19"},
   {"id":"q05","chapterId":"ch07","type":"single","question":"R1 的蒸馏阶段使用什么训练方式？","options":["强化学习","监督微调","蒙特卡洛树搜索","过程奖励模型"],"answer":1,"explain":"蒸馏阶段用 R1 生成的数据做 SFT，不再跑 RL。","relatedConceptId":"c21"},
   {"id":"q06","chapterId":"ch07","type":"single","question":"论文明确列为失败尝试的是哪一项？","options":["GRPO","过程奖励模型（PRM）","冷启动","拒绝采样"],"answer":1,"explain":"论文的 Unsuccessful Attempts 节写了 PRM 和 MCTS 的失败。","relatedConceptId":"c17"},
   {"id":"q07","chapterId":"ch08","type":"single","question":"V4 的 CSA 压缩率是多少？","options":["2:1","4:1","64:1","128:1"],"answer":1,"explain":"CSA 每 4 个 token 压成 1 条，HCA 是 128:1。","relatedConceptId":"c22"},
   {"id":"q08","chapterId":"ch08","type":"single","question":"V4 的 HCA 压缩率是多少？","options":["2:1","4:1","64:1","128:1"],"answer":3,"explain":"HCA 每 128 个 token 压成 1 条，压缩后做稠密注意力。","relatedConceptId":"c23"},
   {"id":"q09","chapterId":"ch08","type":"single","question":"mHC 的混合矩阵被约束成什么？","options":["只有行和为 1","双随机矩阵","正交矩阵","稀疏矩阵"],"answer":1,"explain":"双随机要求行和、列和都为 1，元素非负。","relatedConceptId":"c24"},
   {"id":"q10","chapterId":"ch09","type":"single","question":"V4.1 的 CED 中，解码器全局 KV 来自哪里？","options":["每层自己的隐藏状态","编码器第 20 层的隐藏状态","输入 embedding","Engram 查表"],"answer":1,"explain":"公式 C_l=H_20 W_l^KV，l>20。","relatedConceptId":"c26"},
   {"id":"q11","chapterId":"ch09","type":"blank","question":"V4.1 的全局 KV cache 是每 token ______ 字节。","answer":"890","explain":"论文摘要与图 1 都给出 890 B/token。","relatedConceptId":"c27"},
   {"id":"q12","chapterId":"ch09","type":"single","question":"CSA2 的 Reuse 模式复用了什么？","options":["只复用 Q","主 KV 和 top-k 索引","只复用位置编码","完全重新计算"],"answer":1,"explain":"Reuse 模式连主 KV 和上一层选好的 top-k 索引一起复用。","relatedConceptId":"c27"},
 ],
 "flashcards": [
   {"id":"f01","chapterId":"ch06","front":"R1-Zero 的两类奖励？","back":"准确性奖励（答案对错）和格式奖励（推理/答案标签）。","tags":["R1","奖励"]},
   {"id":"f02","chapterId":"ch06","front":"GRPO 的优势怎么算？","back":"（该回答奖励 - 组内均值）/ 组内标准差。","tags":["R1","GRPO"]},
   {"id":"f03","chapterId":"ch06","front":"“aha moment”指什么？","back":"训练中模型自发出现停下来重新检查、反思的行为。","tags":["R1","现象"]},
   {"id":"f04","chapterId":"ch06","front":"R1-Zero 不能直接上线的原因？","back":"可读性差、中英混杂、格式不合规。","tags":["R1","局限"]},
   {"id":"f05","chapterId":"ch07","front":"冷启动解决什么问题？","back":"用几千条高质量长链推理稳定格式和可读性。","tags":["R1","冷启动"]},
   {"id":"f06","chapterId":"ch07","front":"R1 的四个训练阶段？","back":"冷启动 SFT → 推理 RL → 拒绝采样 SFT → 推理+通用 RL。","tags":["R1","流程"]},
   {"id":"f07","chapterId":"ch07","front":"R1 的 SFT 数据规模？","back":"约 80 万条，60 万推理 + 20 万通用。","tags":["R1","数据"]},
   {"id":"f08","chapterId":"ch07","front":"R1 蒸馏用什么数据、什么方式？","back":"R1 生成并筛选约 8 万条，学生做 SFT。","tags":["R1","蒸馏"]},
   {"id":"f09","chapterId":"ch08","front":"CSA 的两个动作？","back":"每 4 token 压 1 条 + top-k 稀疏选择。","tags":["V4","CSA"]},
   {"id":"f10","chapterId":"ch08","front":"HCA 为什么不做稀疏？","back":"压缩到 1/128 后候选很少，稠密算也可接受。","tags":["V4","HCA"]},
   {"id":"f11","chapterId":"ch08","front":"mHC 为什么用双随机约束？","back":"保证混合是凸组合，不放大信号，训练稳定。","tags":["V4","mHC"]},
   {"id":"f12","chapterId":"ch08","front":"Muon 和 AdamW 的核心区别？","back":"Muon 对梯度矩阵整体正交化，AdamW 逐元素自适应。","tags":["V4","优化器"]},
   {"id":"f13","chapterId":"ch09","front":"CED 的 prefill 为什么能减半？","back":"只算前 20 层编码器，解码器全局 KV 由 H20 投影。","tags":["V4.1","CED"]},
   {"id":"f14","chapterId":"ch09","front":"CSA2 的三种模式？","back":"Full（完整算）、Reindex（复用 KV 重选 top-k）、Reuse（复用 KV 和索引）。","tags":["V4.1","CSA2"]},
   {"id":"f15","chapterId":"ch09","front":"Engram 怎么省计算？","back":"N-gram 哈希查表，O(1) 内存访问替代矩阵乘法。","tags":["V4.1","Engram"]},
   {"id":"f16","chapterId":"ch09","front":"DSpark 和 MTP 的分工？","back":"MTP 偏训练信号，DSpark 是独立训练的推理 drafter。","tags":["V4.1","DSpark"]},
 ],
 "patterns": """# 模式与框架库

## 框架：读论文五问
问题是什么 → 方法核心改了什么 → 数据从哪来 → 实验证明了什么 → 作者承认的局限是什么。

## 框架：实验表三分类
主结果（和基线比）、消融（去掉组件看掉多少）、训练曲线（看机制）。三类不能混读。

## 决策规则
- 先看基线是不是同一个基座，再看提升幅度。
- 先看评测是 pass@1 还是 pass@k，再比较分数。
- 作者没做的实验，通常就是局限。

## 反模式
- 只看摘要的最高分。
- 把“作者解释”当成“实验结论”。
- 把不同论文的 benchmark 直接横比。
""",
 "cheatsheet": """# 速查表

## 关键数字
| 项目 | 数值 |
|---|---|
| R1-Zero AIME 2024 | 15.6% → 71.0% |
| R1 AIME 2024 | 79.8% |
| R1 MATH-500 | 97.3% |
| R1 冷启动数据 | 几千条 |
| R1 SFT 数据 | 约 80 万条（60 万推理 + 20 万通用） |
| R1 蒸馏数据 | 约 8 万条 |
| V4-Pro | 1.6T / 49B，61 层 |
| V4-Flash | 284B / 13B，43 层 |
| CSA 压缩率 | 4:1 |
| HCA 压缩率 | 128:1 |
| V4 1M 上下文 | Pro 27% FLOPs / 10% KV；Flash 10% / 7%（vs V3.2） |
| V4.1-Flash | 552B + 196B Engram，prefill 8B / decode 16B |
| V4.1 全局 KV | 890 B/token |
| V4.1 持久 KV | 约 V4-Flash 的 1/8 |

## 公式
| 场景 | 内容 |
|---|---|
| GRPO 优势 | $A_i=(r_i-\\bar r)/\\mathrm{std}(r)$ |
| 压缩注意力 | 每 m 个 token 加权压成 1 条 |
| OPD | $\\sum_i w_i D_{KL}(\\pi_\\theta\\|\\pi_{E_i})$ |
""",
})

# ============================ Book 3 ============================
BOOKS.append({
 "slug": "deepseek-architecture",
 "title": "架构阐释：三代模型的设计逻辑",
 "subtitle": "用“瓶颈—机制—代价”解释 V3/R1、V4、V4.1 的每一次架构改动",
 "book": {"title": "架构阐释：三代模型的设计逻辑", "author": "本课程整理", "source": [
     "DeepSeek-V3（arXiv:2412.19437）",
     "DeepSeek-R1（arXiv:2501.12948）",
     "DeepSeek-V4（arXiv:2606.19348）",
     "DeepSeek-V4.1-Flash（arXiv:2609.19969）"]},
 "audience": "读完论文拆解篇、想建立架构判断力的读者",
 "goal": "能对任意长上下文模型做瓶颈分析、组件拆解和选型评审",
 "dir": "03-architecture",
 "learningPath": [
   {"step":"01","title":"三代总览与注意力演进","chapterIds":["ch10"],"checkpoint":"能画出注意力演进线并说出每步解决什么"},
   {"step":"02","title":"效率组件的设计逻辑","chapterIds":["ch11"],"checkpoint":"能解释 MoE、mHC、Muon、Engram 各自的分工"},
   {"step":"03","title":"训练与后训练","chapterIds":["ch12"],"checkpoint":"能对比 R1 的 RL 与 V4/V4.1 的 OPD"},
   {"step":"04","title":"综合检验：架构评审","chapterIds":["ch13"],"checkpoint":"完成一份有数字支撑的选型报告"},
   {"step":"05","title":"附录：1M 上下文选型算例","chapterIds":["ch14"],"checkpoint":"能独立算出单序列与并发 KV，并写出选型报告"},
 ],
 "chapters": [
   {"id":"ch10","title":"第 10 章：三代架构总览：瓶颈迁移与注意力演进","file":"chapters/ch10-overview.md","difficulty":3,"source":"DeepSeek-V3/V4/V4.1 技术报告","prerequisites":[]},
   {"id":"ch11","title":"第 11 章：效率组件：MoE、mHC、Muon、Engram、DSpark","file":"chapters/ch11-components.md","difficulty":3,"source":"DeepSeek-V4/V4.1 技术报告","prerequisites":["ch10"]},
   {"id":"ch12","title":"第 12 章：训练与后训练：预训练、RL、蒸馏、数据工程","file":"chapters/ch12-training.md","difficulty":3,"source":"DeepSeek-R1/V4/V4.1 技术报告","prerequisites":["ch11"]},
   {"id":"ch13","title":"第 13 章：综合检验：写一份架构评审报告","file":"chapters/ch13-review.md","difficulty":3,"source":"本课程整理 · 综合任务","prerequisites":["ch12"]},
   {"id":"ch14","title":"附录：1M 上下文选型算例","file":"chapters/ch14-selection.md","difficulty":2,"source":"本课程整理 · 选型附录","prerequisites":["ch13"]},
 ],
 "concepts": [
   {"id":"c32","title":"推理 FLOPs","file":"concepts/c32-inference-flops.md","chapterIds":["ch10","ch13"],"difficulty":"高难","source":"DeepSeek-V4/V4.1 技术报告","prerequisites":[]},
   {"id":"c33","title":"奖励模型","file":"concepts/c33-reward-model.md","chapterIds":["ch12"],"difficulty":"进阶","source":"DeepSeek-R1/V4 技术报告","prerequisites":[]},
   {"id":"c34","title":"OPD（在线策略蒸馏）","file":"concepts/c34-opd.md","chapterIds":["ch12"],"difficulty":"高难","source":"DeepSeek-V4/V4.1 技术报告 §5","prerequisites":["c33"]},
   {"id":"c35","title":"数据工程","file":"concepts/c35-data-engineering.md","chapterIds":["ch12"],"difficulty":"进阶","source":"DeepSeek-V4.1 论文 §5","prerequisites":[]},
   {"id":"c36","title":"架构取舍","file":"concepts/c36-architecture-tradeoffs.md","chapterIds":["ch10","ch11","ch13"],"difficulty":"进阶","source":"本课程整理 · 架构分析","prerequisites":["c32"]},
 ],
 "glossary": [
   {"term":"瓶颈迁移","def":"部署瓶颈从 KV cache 转向 FLOPs 再转向 prefill/带宽。","chapterId":"ch10"},
   {"term":"激活参数","def":"单个 token 实际参与计算的参数。","chapterId":"ch10"},
   {"term":"总参数","def":"模型全部参数，MoE 中远大于激活参数。","chapterId":"ch10"},
   {"term":"非对称架构","def":"prefill 和 decode 走不同计算路径的架构。","chapterId":"ch10"},
   {"term":"专家并行","def":"把 MoE 专家分布到不同设备上。","chapterId":"ch11"},
   {"term":"路由","def":"决定 token 进入哪些专家的机制。","chapterId":"ch11"},
   {"term":"双随机矩阵","def":"行和、列和都为 1 的非负矩阵。","chapterId":"ch11"},
   {"term":"正交化","def":"把梯度矩阵的奇异值拉到接近 1。","chapterId":"ch11"},
   {"term":"压缩维度","def":"条目大小、序列长度、层数、位宽四个可压缩方向。","chapterId":"ch11"},
   {"term":"prefill","def":"读入整段输入并建立 KV cache 的阶段。","chapterId":"ch12"},
   {"term":"decode","def":"逐 token 生成输出的阶段。","chapterId":"ch12"},
   {"term":"OPD","def":"学生在自己轨迹上向多个教师做全词表蒸馏。","chapterId":"ch12"},
   {"term":"GRM","def":"生成式奖励模型，模型自己生成评分理由和分数。","chapterId":"ch12"},
   {"term":"DSec","def":"V4.1 用于大规模智能体 RL 的弹性计算沙箱。","chapterId":"ch12"},
   {"term":"任务三元组","def":"问题、环境、验证系统。","chapterId":"ch12"},
   {"term":"effort","def":"1–100 的推理力度标量，控制输出长度。","chapterId":"ch12"},
   {"term":"全局 KV cache","def":"常驻 HBM 的主 KV 缓存。","chapterId":"ch13"},
   {"term":"持久 KV cache","def":"放 SSD/主机内存、用于前缀复用的缓存。","chapterId":"ch13"},
   {"term":"算术强度","def":"每字节内存访问对应的计算量。","chapterId":"ch13"},
   {"term":"选型","def":"在负载、成本、质量约束下选最合适的模型。","chapterId":"ch13"},
 ],
 "quizzes": [
   {"id":"q01","chapterId":"ch10","type":"single","question":"R1 相对于 V3 的主要变化是什么？","options":["注意力结构","后训练方法","层数","词表大小"],"answer":1,"explain":"R1 的模型结构与 V3 相同，变化在 RL 后训练。","relatedConceptId":"c36"},
   {"id":"q02","chapterId":"ch10","type":"single","question":"V4 的 CSA 和 HCA 压缩率分别是？","options":["4:1 和 128:1","2:1 和 64:1","8:1 和 256:1","1:1 和 1:1"],"answer":0,"explain":"CSA 4:1，HCA 128:1。","relatedConceptId":"c36"},
   {"id":"q03","chapterId":"ch10","type":"single","question":"V4.1-Flash 的 prefill 激活参数约是多少？","options":["8B","13B","16B","49B"],"answer":0,"explain":"CED 让 prefill 只跑编码器路径，约 8B；decode 16B。","relatedConceptId":"c32"},
   {"id":"q04","chapterId":"ch11","type":"single","question":"MoE 主要省的是哪一项？","options":["显存占用","单 token 计算量","通信量","词表大小"],"answer":1,"explain":"MoE 只激活部分专家，计算按激活参数算，但所有权重仍要存。","relatedConceptId":"c36"},
   {"id":"q05","chapterId":"ch11","type":"single","question":"mHC 的混合矩阵被约束成什么？","options":["正交矩阵","双随机矩阵","对角矩阵","稀疏矩阵"],"answer":1,"explain":"行和、列和为 1，非负，保证混合不放大信号。","relatedConceptId":"c36"},
   {"id":"q06","chapterId":"ch11","type":"single","question":"Engram 的核心机制是什么？","options":["矩阵乘法","哈希查表","注意力","卷积"],"answer":1,"explain":"Engram 用 N-gram 哈希查表，O(1) 内存访问。","relatedConceptId":"c36"},
   {"id":"q07","chapterId":"ch12","type":"single","question":"V4 用什么方法合并多个领域专家？","options":["权重平均","混合 RL","在线策略蒸馏（OPD）","直接 SFT"],"answer":2,"explain":"V4 用 10 多个教师做全词表 OPD。","relatedConceptId":"c34"},
   {"id":"q08","chapterId":"ch12","type":"single","question":"V4.1 后训练的主要创新在哪里？","options":["新的 RL 算法","新的 OPD 算法","数据与环境流水线","新的 SFT 损失"],"answer":2,"explain":"论文明确说算法没有新东西，收益来自数据与环境工程。","relatedConceptId":"c35"},
   {"id":"q09","chapterId":"ch12","type":"single","question":"R1 四阶段中的第一步是什么？","options":["推理 RL","冷启动 SFT","拒绝采样","蒸馏"],"answer":1,"explain":"R1 先做几千条冷启动 SFT，再做 RL。","relatedConceptId":"c35"},
   {"id":"q10","chapterId":"ch13","type":"single","question":"1M token、每 token 890 B，单请求全局 KV 约多少？","options":["89 MB","890 MB","8.9 GB","89 GB"],"answer":1,"explain":"10^6 × 890 = 8.9×10^8 字节，约 890 MB。","relatedConceptId":"c32"},
   {"id":"q11","chapterId":"ch13","type":"single","question":"输入/输出比 200:1 时，哪种架构收益最明显？","options":["MoE","CED","Engram","mHC"],"answer":1,"explain":"CED 省的是 prefill，输入占比越高收益越大。","relatedConceptId":"c32"},
   {"id":"q12","chapterId":"ch13","type":"single","question":"架构选型的原则是什么？","options":["永远选最强模型","满足要求下总成本最低","压缩率最高","参数最大"],"answer":1,"explain":"选型是够用 + 总成本最低，不是最强。","relatedConceptId":"c36"},
 ],
 "flashcards": [
   {"id":"f01","chapterId":"ch10","front":"R1 改变了模型架构吗？","back":"没有，R1 结构与 V3 相同，变的是后训练。","tags":["架构","R1"]},
   {"id":"f02","chapterId":"ch10","front":"三代架构的瓶颈迁移顺序？","back":"KV cache → 注意力 FLOPs + KV → prefill + KV 存储/带宽。","tags":["架构","瓶颈"]},
   {"id":"f03","chapterId":"ch10","front":"MLA 解决什么？","back":"用低维潜向量压 KV cache，支撑 128K 上下文。","tags":["架构","MLA"]},
   {"id":"f04","chapterId":"ch10","front":"CSA2 多了哪个压缩维度？","back":"层维度：跨层复用主 KV、索引器 K 和 top-k 索引。","tags":["架构","CSA2"]},
   {"id":"f05","chapterId":"ch11","front":"MoE 的总参数和激活参数区别？","back":"总参数是全部专家，激活参数是单 token 实际用到的部分。","tags":["组件","MoE"]},
   {"id":"f06","chapterId":"ch11","front":"mHC 的约束和投影方法？","back":"双随机矩阵，Sinkhorn-Knopp 迭代。","tags":["组件","mHC"]},
   {"id":"f07","chapterId":"ch11","front":"Muon 怎么更新？","back":"Newton-Schulz 正交化梯度矩阵，再动量更新。","tags":["组件","Muon"]},
   {"id":"f08","chapterId":"ch11","front":"Engram 为什么 O(1)？","back":"哈希查表，不需要矩阵乘法。","tags":["组件","Engram"]},
   {"id":"f09","chapterId":"ch12","front":"R1 后训练四阶段？","back":"冷启动 SFT → 推理 RL → 拒绝采样 SFT → 推理+通用 RL。","tags":["训练","R1"]},
   {"id":"f10","chapterId":"ch12","front":"V4 后训练两阶段？","back":"领域专家 SFT+GRPO → 多教师 OPD。","tags":["训练","V4"]},
   {"id":"f11","chapterId":"ch12","front":"OPD 的“在线”指什么？","back":"轨迹由学生自己生成，教师在这些轨迹上给 logits。","tags":["训练","OPD"]},
   {"id":"f12","chapterId":"ch12","front":"V4 的稳定性手段？","back":"Anticipatory Routing、SwiGLU Clamping、mHC、Muon。","tags":["训练","稳定性"]},
   {"id":"f13","chapterId":"ch13","front":"单请求 KV 怎么算？","back":"token 数 × 每 token 字节数。","tags":["选型","KV"]},
   {"id":"f14","chapterId":"ch13","front":"CED 适合什么负载？","back":"输入密集、prefill 占比高的智能体负载。","tags":["选型","CED"]},
   {"id":"f15","chapterId":"ch13","front":"选型三问？","back":"瓶颈是什么、代价是什么、实验验证了什么。","tags":["选型","方法"]},
   {"id":"f16","chapterId":"ch13","front":"评审报告六节？","back":"画像、瓶颈、对比、建议、风险、结论。","tags":["选型","报告"]},
 ],
 "patterns": """# 模式与框架库

## 框架：瓶颈—机制—代价
解释任何架构改动：它替哪笔账还债、用什么机制、付出什么代价。三个都说清才算解释。

## 框架：多维压缩
KV cache 可从条目大小、序列长度、层数、位宽四个维度压缩；先看论文压了哪几个维度。

## 决策规则
- 先量化负载，再选模型。
- 只为自己用得上的能力付费。
- FLOPs、KV、延迟、成本分开算。

## 反模式
- 把“最新一代”当成“最适合”。
- 把压缩率当成唯一指标。
- 用 FLOPs 估算代替端到端实测。
""",
 "cheatsheet": """# 速查表

## 关键数字
| 项目 | 数值 |
|---|---|
| V3 | 671B / 37B，61 层，MLA，14.8T token |
| V4-Pro | 1.6T / 49B，61 层，CSA+HCA，33T token |
| V4-Flash | 284B / 13B，43 层，CSA+HCA，32T token |
| V4.1-Flash | 552B + 196B Engram，40 层，prefill 8B / decode 16B，45T token |
| V4 1M 效率 | Pro 27% FLOPs / 10% KV；Flash 10% / 7% |
| V4.1 全局 KV | 890 B/token；持久 KV 约 V4-Flash 的 1/8 |
| CSA / HCA | 4:1 / 128:1 |
| R1 后训练 | 冷启动 → RL → 拒绝采样 → RL |
| V4 后训练 | 专家 SFT+GRPO → 10+ 教师 OPD |
| V4.1 后训练 | SFT+RL → 40+ 教师 OPD |

## 公式
| 场景 | 内容 |
|---|---|
| 单请求 KV | token 数 × 每 token 字节 |
| 延迟近似 | max(FLOPs/算力, 字节/带宽) + 调度 |
| OPD | $\\sum_i w_i D_{KL}(\\pi_\\theta\\|\\pi_{E_i})$ |
""",
})


def write_manifest(book):
    d = os.path.join(ROOT, book["dir"])
    manifest = {
        "slug": book["slug"],
        "title": book["title"],
        "subtitle": book["subtitle"],
        "book": book["book"],
        "audience": book["audience"],
        "goal": book["goal"],
        "learningPath": book["learningPath"],
        "chapters": book["chapters"],
        "concepts": book["concepts"],
        "glossary": book["glossary"],
        "patterns": {"file": "patterns.md"},
        "cheatsheet": {"file": "cheatsheet.md"},
        "quizzes": book["quizzes"],
        "flashcards": book["flashcards"],
    }
    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # quiz.md
    lines = [f"# {book['title']} 测验", ""]
    by_ch = {}
    for q in book["quizzes"]:
        by_ch.setdefault(q["chapterId"], []).append(q)
    for ch in book["chapters"]:
        qs = by_ch.get(ch["id"], [])
        if not qs:
            continue
        lines.append(f"## {ch['title']}")
        for i, q in enumerate(qs, 1):
            lines.append(f"### Q{i}. {q['question']}")
            if q["type"] in ("single", "multi"):
                for oi, o in enumerate(q.get("options", [])):
                    lines.append(f"- {'ABCD'[oi]}. {o}")
                if q["type"] == "single":
                    lines.append(f"**答案**：{'ABCD'[q['answer']]}")
                else:
                    lines.append(f"**答案**：{q['answer']}")
            else:
                lines.append(f"**答案**：{q['answer']}")
            lines.append(f"**解析**：{q['explain']}")
            lines.append("")
    with open(os.path.join(d, "quiz.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # flashcards.md
    lines = [f"# {book['title']} 抽认卡", ""]
    by_ch = {}
    for c in book["flashcards"]:
        by_ch.setdefault(c["chapterId"], []).append(c)
    for ch in book["chapters"]:
        cs = by_ch.get(ch["id"], [])
        if not cs:
            continue
        lines.append(f"## {ch['title']}")
        for c in cs:
            lines.append(f"### 卡片：{c['front']}")
            lines.append(f"- **背面**：{c['back']}")
            lines.append(f"- **标签**：{', '.join(c.get('tags', []))}")
            lines.append(f"- **章节**：{c['chapterId']}")
            lines.append("")
    with open(os.path.join(d, "flashcards.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # glossary.md
    lines = ["# 术语表", "", "| 术语 | 白话定义 | 首次出现 | 章节 |", "|---|---|---|---|"]
    ch_title = {c["id"]: c["title"] for c in book["chapters"]}
    for g in book["glossary"]:
        lines.append(f"| {g['term']} | {g['def']} | {g['chapterId']} | {ch_title.get(g['chapterId'], g['chapterId'])} |")
    with open(os.path.join(d, "glossary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # patterns / cheatsheet
    with open(os.path.join(d, "patterns.md"), "w", encoding="utf-8") as f:
        f.write(book["patterns"])
    with open(os.path.join(d, "cheatsheet.md"), "w", encoding="utf-8") as f:
        f.write(book["cheatsheet"])

    # paths/learn.md
    os.makedirs(os.path.join(d, "paths"), exist_ok=True)
    lines = [f"# 学习路径：{book['title']}", "",
             f"面向{book['audience']}。目标：{book['goal']}。", "", "## 路径总览", ""]
    for step in book["learningPath"]:
        lines.append(f"{step['step']}. **{step['title']}** → {', '.join(step['chapterIds'])}")
    lines.append("")
    for step in book["learningPath"]:
        lines.append(f"## 步骤 {step['step']}：{step['title']}")
        lines.append(f"**目标**：完成本章学习目标。")
        lines.append(f"**阅读**：{', '.join(step['chapterIds'])}")
        lines.append(f"**检查点**：{step['checkpoint']}")
        lines.append("")
    with open(os.path.join(d, "paths", "learn.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def validate(book):
    d = os.path.join(ROOT, book["dir"])
    ids = {c["id"] for c in book["chapters"]} | {c["id"] for c in book["concepts"]}
    graph = {}
    for item in book["chapters"] + book["concepts"]:
        prereqs = []
        for p in item.get("prerequisites", []):
            prereqs.append(p["id"] if isinstance(p, dict) else p)
        graph[item["id"]] = prereqs
    for item in book["concepts"]:
        if item.get("depthFragment"):
            fp = os.path.join(d, item["depthFragment"])
            if not os.path.exists(fp):
                raise SystemExit(f"depthFragment 不存在: {fp}")
    # 检测环
    visiting, done = set(), set()
    def dfs(n):
        if n in done: return
        if n in visiting:
            raise SystemExit(f"依赖图存在环: {n} in {book['slug']}")
        visiting.add(n)
        for p in graph.get(n, []):
            if p in graph:
                dfs(p)
        visiting.remove(n); done.add(n)
    for n in graph:
        dfs(n)
    print(f"✓ {book['slug']}: {len(book['chapters'])} 章 / {len(book['concepts'])} 概念 / {len(book['quizzes'])} 测验 / {len(book['flashcards'])} 卡片 / {len(book['glossary'])} 术语")


if __name__ == "__main__":
    for b in BOOKS:
        validate(b)
        write_manifest(b)
    print("完成：三本书的 manifest.json 与配套 Markdown 已生成")
