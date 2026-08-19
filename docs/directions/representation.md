---
title: Representation / Activation
tags:
  - Residual stream
  - Activation steering
  - Representation editing
---

# Representation / Activation

本方向研究错误对象或属性语义何时被写入 residual stream，以及 attention、MLP、KV cache 与 LM head 如何共同放大该信号。

## 研究问题

- 幻觉语义在中间层是否已经线性可读？
- head output 加入 residual stream 后，MLP 是纠错、保持还是放大？
- 单一全局 steering vector 是否混合了事实性与任务语义？
- rank-one、low-rank 与实例级子空间编辑的效用—保真权衡如何？

## 当前状态

现有附件中的 IR Edit、Dynamic Multimodal Activation Steering 等论文已进入[待读队列](../library/reading-queue.md)，尚未把 PDF 自动转换成经核对的 Paper Card。

## 建议输出

每次 representation intervention 至少保存：layer、token position、direction norm、projection coefficient、pre/post logits、KL divergence、recall 与文本退化指标。

