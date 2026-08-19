---
title: Attention Head / Path
tags:
  - Attention head
  - Causal pathway
  - Intervention
---

# Attention Head / Path

## 核心问题

- vision-aware head 是否在幻觉发生前失活或被其他路径覆盖？
- 幻觉相关 head 的作用来自 attention routing，还是 value/output 中写入的语义？
- 静态全程缩放为什么容易降低 recall、产生重复或拉长输出？

## 关键阅读

- [Role-Break](../papers/role-break-attention-heads.md)：将每个 head 相对自身 faithful source-allocation baseline 的偏离作为统一检测特征。
- [Same Attention, Different Truths](../papers/same-attention-different-truths.md)：说明 attention quantity 本身不能区分 grounded 与 hallucinated object，需要读取高注意区域语义。
- [Modular Attribution & Intervention](../papers/modular-attribution-intervention.md)：组件消融与 hallucination heads。
- [Vision-aware Head Divergence](../papers/vision-aware-head-divergence.md)：有图/无图 head-output divergence。
- [Intervene-All-Paths](../papers/intervene-all-paths.md)：I2I、I2T、T2T 路径的联合识别与干预。
- [OPERA](../papers/opera.md)：summary-token aggregation 与 over-trust penalty。

## 推荐因果验证

1. 对高分 head、随机 head 与低分 head 做等数量消融。
2. 分开修改 attention weights、head value/output 和 residual contribution。
3. 只在 hallucination onset 前的局部窗口干预。
4. 在原图、空图和对象删除图之间做 head-output activation patching。
5. 同时画 CHAIRi–Recall、CHAIRs–length 和 hallucination–repetition 曲线。
