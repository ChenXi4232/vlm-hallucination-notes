---
title: 方法论文
tags:
  - Method
---

# 方法论文

本页是已通过 Deep Paper Note 校验的方法目录；方法细节、结果与局限只在对应论文页维护。当前共 15 篇，全部带有可追溯的方法概览图。

## Logit / decoding

- [Same Attention, Different Truths](../papers/same-attention-different-truths.md) — LLCC + HARM + VEED 的分型检测与缓解。
- [VISOR](../papers/visor.md) — 属性 logit signal 分解与机制路由修复。
- [M3ID](../papers/m3id.md) — visual prompt amplification。
- [Self-Introspective Decoding](../papers/self-introspective-decoding.md) — least-important token contrastive branch。
- [Curing Semantic Drift](../papers/curing-semantic-drift.md) — external visual referee 与 dynamic logits calibration。
- [OPERA](../papers/opera.md) — over-trust penalty 与 retrospection-allocation。
- [MARINE](../papers/marine-image-grounded-guidance.md) — 外部 detector/tagger guidance 与双分支 logit 控制。

## Head / path intervention

- [Role-Break](../papers/role-break-attention-heads.md) — faithful head role residual 与轻量线性 detector。
- [Modular Attribution & Intervention](../papers/modular-attribution-intervention.md) — hallucination head attribution 与 AD-HH/TF-HH。
- [Vision-aware Head Divergence](../papers/vision-aware-head-divergence.md) — VHD 诊断与 VHR 增强。
- [Intervene-All-Paths](../papers/intervene-all-paths.md) — 多因果路径联合干预。
- [Hallucination Begins Where Saliency Drops](../papers/hallucination-begins-where-saliency-drops.md) — attention×gradient 诊断、SGRS 与 LocoRE。

## Representation editing

- [Beyond Global Editing](../papers/beyond-global-editing.md) — cluster-specific HalluSpaces 与 per-instance adaptive projection。
- [HIRE](../papers/hire-intermediate-representation-edit.md) — learned Editor、token Router 与可调表示编辑。
- [DMAS](../papers/dynamic-multimodal-activation-steering.md) — 语义动态 truthfulness vector 与逐图 visual vector。

## Baseline 选择建议

| 研究层级 | 最小 baseline 组 | 主要用途 |
|---|---|---|
| Logit | Vanilla + M3ID/SID + MARINE | 比较内部反事实与外部视觉 guidance |
| Head | Vanilla + random-head + VHD/VHR + AllPath + LocoRE | 验证头集合、路径与局部历史干预 |
| Representation | global vector + HIRE + DMAS + multi-subspace | 拆解学习式、检索式与逐样本方向 |
| Dynamic | static intervention + risk-gated intervention | 检查收益是否来自避免全程过强干预 |
