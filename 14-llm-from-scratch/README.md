# LLM 从零实现：训练、对齐与部署

第 14 本分册。目标不是再讲一遍 Transformer，而是把 tokenizer、tiny GPT、预训练、SFT、LoRA、偏好对齐、KV cache、RAG 和评测串成一条能验收的链路。

## 适合谁

- 学完《神经网络》或《深度学习入门》，会 Python 和矩阵乘法；
- 想从“会调 API”走到“知道权重里发生了什么”；
- 不需要先有 GPU：前 6 章可在 CPU 上做最小实验。

## 读法

1. 第 1–3 章：数据与 tokenizer，先把输入管线跑通；
2. 第 4–6 章：embedding、attention、GPT 组装，每章抄一遍形状；
3. 第 7–8 章：预训练与 SFT，做单 batch 过拟合；
4. 第 9–10 章：LoRA 与偏好对齐，理解“改行为”而不是“灌知识”；
5. 第 11–13 章：推理、RAG/Agent、评测与安全；
6. 第 14 章：按硬件选一条最小可复现路线。

## 开源来源与边界

本分册是原创中文讲解，参考了以下公开课程的目录与教学思路，不整段复制其正文：

- `LLMs-from-scratch`：7 章从注意力到指令微调，代码结构清楚；
- `Modern LLM Notebook`：23 个 notebook，覆盖训练、对齐、推理与前沿；
- `Happy-LLM`：中文 8 章，从 NLP 到 215M LLaMA2；
- `MiniMind`：Apache-2.0，64M 小模型全链路；
- Hugging Face `smol-course`：小模型 SFT/DPO/VLM 本地实验。

各项目许可不同：MIT/Apache-2.0 可复用代码；CC-BY-NC-SA 只能按非商业条款分享；fast.ai 的 prose 有额外限制。引用不等于授权，商用前读 LICENSE。

## 验收

完成本分册后，你至少应有：

- 一份 tokenizer 编码样例与 tokens/字符统计；
- 一个能过拟合单 batch 的 tiny GPT；
- 一次 SFT 和一次 LoRA 的 checkpoint；
- 一张 KV cache/显存账本；
- 一份评测报告，含失败样本和污染检查。
