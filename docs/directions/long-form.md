---
title: Long-form / Semantic Drift
tags:
  - Long-form generation
  - Semantic drift
  - Error accumulation
---

# Long-form / Semantic Drift

长文本幻觉不一定是某个对象词的孤立错误，而可能是视觉条件随自回归上下文增长而被逐步稀释。

## 关键阅读

- [Curing Semantic Drift](../papers/curing-semantic-drift.md)：动态视觉基线与 token selection failure。
- [OPERA](../papers/opera.md)：summary-token over-trust 与 rollback。
- [M3ID](../papers/m3id.md)：conditioning dilution 与视觉 prompt amplification。
- [Hallucination Begins Where Saliency Drops](../papers/hallucination-begins-where-saliency-drops.md)：output-token saliency drop 与局部上下文记忆强化。

## 建议分析轴

- 按 token position 对齐 visual-dependence curve。
- 以 hallucination onset 为零点观察前后窗口。
- 区分 candidate absence 与 candidate selection failure。
- 报告最大长度触发率、重复片段率和平均对象覆盖。
