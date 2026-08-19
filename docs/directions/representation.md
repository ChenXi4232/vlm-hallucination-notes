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

## 关键阅读

- [Beyond Global Editing](../papers/beyond-global-editing.md)：将差分聚类为多个低秩 HalluSpaces，再用测试样本的 mask response 动态混合 projector。
- [VISOR](../papers/visor.md)：用逐层视觉 margin SNR 定位材质属性信号在 decoder 晚层的坍塌。

IR Edit、Dynamic Multimodal Activation Steering 等其他论文仍在[待读队列](../library/reading-queue.md)，尚未转换成经核对的 Deep Paper Note。

## 建议输出

每次 representation intervention 至少保存：layer、token position、direction norm、projection coefficient、pre/post logits、KL divergence、recall 与文本退化指标。
