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

- [HulluEdit](../papers/hulluedit.md)：每个生成步用视觉token与文本cache构造正交低秩子空间；需区分“保护定义内投影”与“保护全部视觉语义”。
- [VES-RFT](../papers/ves-rft.md)：把有图/无图决策熵差变成训练奖励，并用 verifier 约束“正确地依赖图像”。
- [Pixels Versus Priors](../papers/pixels-versus-priors.md)：以视觉反事实观察 pixel/prior 的逐层竞争，并构造双向 PvP steering vectors。
- [MESA](../papers/mesa-mitigating-entangled-steering.md)：显式分离 hallucination steering 与内容语义，减少全局方向带来的能力损失。
- [Beyond Global Editing](../papers/beyond-global-editing.md)：将差分聚类为多个低秩 HalluSpaces，再用测试样本的 mask response 动态混合 projector。
- [HIRE](../papers/hire-intermediate-representation-edit.md)：用 learned Editor 生成 token-specific direction，再由 Router 选择性触发。
- [DMAS](../papers/dynamic-multimodal-activation-steering.md)：语义检索 truthfulness vector 与逐图 visual-perception vector 的 head-level 注入。
- [VISOR](../papers/visor.md)：用逐层视觉 margin SNR 定位材质属性信号在 decoder 晚层的坍塌。

## 建议输出

每次 representation intervention 至少保存：layer、token position、direction norm、projection coefficient、pre/post logits、KL divergence、recall 与文本退化指标。

在线子空间还应记录：SVD rank/奇异值、每步子空间夹角、norm/blend、门控触发率、真实/错配图投影差，以及论文公式与发布代码的映射。

## 初始 KV cache

[PTI](../papers/prefill-time-intervention.md) 将干预移至prefill，只修改初始图文缓存；与逐步steering的对比应同时控制方向、位置、强度和输出长度。CHAIR下降不代表F1无损。
