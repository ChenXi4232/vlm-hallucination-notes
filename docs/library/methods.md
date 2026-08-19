---
title: 方法论文
tags:
  - Method
---

# 方法论文

## Logit / decoding

- [M3ID](../papers/m3id.md) — visual prompt amplification。
- [Self-Introspective Decoding](../papers/self-introspective-decoding.md) — least-important token contrastive branch。
- [Curing Semantic Drift](../papers/curing-semantic-drift.md) — external visual referee 与 dynamic logits calibration。
- [OPERA](../papers/opera.md) — over-trust penalty 与 retrospection-allocation。

## Head / path intervention

- [Modular Attribution & Intervention](../papers/modular-attribution-intervention.md) — hallucination head attribution 与 AD-HH/TF-HH。
- [Vision-aware Head Divergence](../papers/vision-aware-head-divergence.md) — VHD 诊断与 VHR 增强。
- [Intervene-All-Paths](../papers/intervene-all-paths.md) — 多因果路径联合干预。

## Baseline 选择建议

| 研究层级 | 最小 baseline 组 | 主要用途 |
|---|---|---|
| Logit | Vanilla + VCD/M3ID + SID | 检查对比分支设计是否真正利用视觉差异 |
| Head | Vanilla + random-head + VHD/VHR + AllPath | 验证头集合与干预方向的因果性 |
| Dynamic | static intervention + risk-gated intervention | 检查收益是否来自避免全程过强干预 |
| System | internal detector + external grounding reranker | 比较内部机制信号与外部视觉先验 |

