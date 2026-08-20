---
title: 方法论文
tags:
  - Method
---

# 方法论文

本页是已通过 Deep Paper Note 校验的方法目录；方法细节、主结果、消融与局限只在对应论文页维护。当前共 20 篇，全部带有可追溯的方法概览图与实验登记。

## Logit / decoding

- [Attention-Guided Switching (AGS)](../papers/attention-guided-switching.md) — 以视觉—文本注意力比在显式逻辑与潜在感知之间动态路由。
- [Risk-aware Selective Prompting (RSP)](../papers/risk-aware-selective-prompting.md) — 用校准集学习层级风险分数，只在高风险输入上追加视觉描述提示。
- [Same Attention, Different Truths](../papers/same-attention-different-truths.md) — LLCC + HARM + VEED 的分型检测与缓解。
- [VISOR](../papers/visor.md) — 属性 logit signal 分解与机制路由修复。
- [M3ID](../papers/m3id.md) — visual prompt amplification。
- [Self-Introspective Decoding](../papers/self-introspective-decoding.md) — least-important token contrastive branch。
- [Curing Semantic Drift](../papers/curing-semantic-drift.md) — external visual referee 与 dynamic logits calibration。
- [OPERA](../papers/opera.md) — over-trust penalty 与 retrospection-allocation。
- [MARINE](../papers/marine-image-grounded-guidance.md) — 外部 detector/tagger guidance 与双分支 logit 控制。

## Head / path intervention

- [Attention-Space Contrastive Guidance (ACG)](../papers/attention-space-contrastive-guidance.md) — 在自注意力分布空间构造对比分支，以一次额外注意力计算校正候选分布。
- [CausalLens](../papers/causallens.md) — 用敏感度筛选头，并以多头因果干预增强视觉证据路径。
- [Role-Break](../papers/role-break-attention-heads.md) — faithful head role residual 与轻量线性 detector。
- [Modular Attribution & Intervention](../papers/modular-attribution-intervention.md) — hallucination head attribution 与 AD-HH/TF-HH。
- [Vision-aware Head Divergence](../papers/vision-aware-head-divergence.md) — VHD 诊断与 VHR 增强。
- [Intervene-All-Paths](../papers/intervene-all-paths.md) — 多因果路径联合干预。
- [Hallucination Begins Where Saliency Drops](../papers/hallucination-begins-where-saliency-drops.md) — attention×gradient 诊断、SGRS 与 LocoRE。

## Representation editing

- [MESA](../papers/mesa-mitigating-entangled-steering.md) — 将幻觉方向与内容语义解耦，在保留任务表征的同时执行选择性 steering。
- [Beyond Global Editing](../papers/beyond-global-editing.md) — cluster-specific HalluSpaces 与 per-instance adaptive projection。
- [HIRE](../papers/hire-intermediate-representation-edit.md) — learned Editor、token Router 与可调表示编辑。
- [DMAS](../papers/dynamic-multimodal-activation-steering.md) — 语义动态 truthfulness vector 与逐图 visual vector。

## Baseline 选择建议

| 研究层级 | 最小 baseline 组 | 主要用途 |
|---|---|---|
| Logit | Vanilla + M3ID/SID + MARINE + RSP | 比较内部反事实、外部视觉 guidance 与风险门控 prompting |
| Head | Vanilla + random-head + VHD/VHR + AllPath + LocoRE + ACG/CausalLens | 验证头集合、注意力分布、路径与局部历史干预 |
| Representation | global vector + HIRE + DMAS + MESA + multi-subspace | 拆解学习式、检索式、解耦式与逐样本方向 |
| Dynamic | static intervention + risk-gated intervention | 检查收益是否来自避免全程过强干预 |
