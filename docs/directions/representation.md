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

- [VES-RFT](../papers/ves-rft.md)：把有图/无图决策熵差变成训练奖励，并用 verifier 约束“正确地依赖图像”。
- [Pixels Versus Priors](../papers/pixels-versus-priors.md)：以视觉反事实观察 pixel/prior 的逐层竞争，并构造双向 PvP steering vectors。
- [MESA](../papers/mesa-mitigating-entangled-steering.md)：显式分离 hallucination steering 与内容语义，减少全局方向带来的能力损失。
- [Beyond Global Editing](../papers/beyond-global-editing.md)：将差分聚类为多个低秩 HalluSpaces，再用测试样本的 mask response 动态混合 projector。
- [HIRE](../papers/hire-intermediate-representation-edit.md)：用 learned Editor 生成 token-specific direction，再由 Router 选择性触发。
- [DMAS](../papers/dynamic-multimodal-activation-steering.md)：语义检索 truthfulness vector 与逐图 visual-perception vector 的 head-level 注入。
- [VISOR](../papers/visor.md)：用逐层视觉 margin SNR 定位材质属性信号在 decoder 晚层的坍塌。

## 建议输出

每次 representation intervention 至少保存：layer、token position、direction norm、projection coefficient、pre/post logits、KL divergence、recall 与文本退化指标。
