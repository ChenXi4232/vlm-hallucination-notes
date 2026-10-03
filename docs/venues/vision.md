---
title: CVPR / ICCV / ECCV
tags:
  - CVPR
  - Vision conference
---

# CVPR / ICCV / ECCV

- [Attention-Space Contrastive Guidance](../papers/attention-space-contrastive-guidance.md) — CVPR 2026 Findings，以注意力空间对比分支实现低开销解码 guidance。
- [CausalLens](../papers/causallens.md) — CVPR 2026，以敏感度筛选和多头因果干预缓解幻觉。
- [VES-RFT](../papers/ves-rft.md) — CVPR 2026，以视觉证据熵差和可验证奖励做 GRPO 微调。
- [PAS](../papers/pas-prelim-attention-score.md) — CVPR 2026，以 prelim attention 做对象词级幻觉检测。
- [Same Attention, Different Truths](../papers/same-attention-different-truths.md) — CVPR 2026，以 Logit-Lens 检查高注意区域的证据语义。
- [M3ID](../papers/m3id.md) — CVPR 2024。
- [OPERA](../papers/opera.md) — CVPR 2024 Highlight。

视觉会议中的方法通常更强调 image grounding、caption benchmark 和视觉工具，但仍需检查是否把 CLIP/detector 类别先验误当成 LVLM 内部机制。

## CVPR 主题阅读路径与比较矩阵 {#cvpr}

先明确问题和评测单位，再选择方法；以下比较来自已链接Note及其中原文表号，不按不同实验设置下的分数给论文排名。主会、Findings和Workshop分别登记；Findings不视为CCF目录所称主会正式长文。

| 问题 → 阅读顺序 | 方法族 | 已有证据 | 必查局限 | 可复现基线 / 关系依据 |
|---|---|---|---|---|
| 长输出对象错误 → [M3ID](../papers/m3id.md) → [FLB](../papers/first-logit-boosting.md) | 对比解码 / 首步logit回注 | FLB Tables 1–3同报幻觉、recall与长度 | The-only、β-only、greedy掉覆盖 | FLB直接比较M3ID；Table 1–2 |
| 干预应发生在哪 → [OPERA](../papers/opera.md) → [PTI](../papers/prefill-time-intervention.md) | 解码搜索 / prefill KV | PTI Table 1跨三种解码；Supplement Table 9延迟 | PTI Table 5 F1下降，输出缩短 | PTI在beam设置直接比较OPERA；不是相同机制 |
| 对象证据怎样进入表示 → [ICT](../papers/ict.md) → [PTI](../papers/prefill-time-intervention.md) | steering / KV | PTI按模态、位置、K/V做消融 | 同时改变多变量不能只归因于时机 | PTI Related Work引用ICT；实现均需位置对齐 |
| attention是否等于真证据 → [PAS](../papers/pas-prelim-attention-score.md) → [SADT](../papers/same-attention-different-truths.md) | 对象检测proxy / 语义诊断 | 各Note登记对象词级检测与语义证据 | proxy与因果使用区别、对象词标签 | 本站按相同检测问题组织，不宣称作者互引 |
| 偏好优化数据从哪里来 → [OPA-DPO](../papers/opa-dpo.md) | Training / Alignment | Note登记on-policy偏好数据和比较 | 数据来源、模型policy匹配和recall | 与无需参数训练方法不直接比成本 |

PTI与FLB共享“早期证据如何影响后续输出”的问题，但本轮未发现直接互引，也没有证据证明二者机制等价。阅读时先查各Note的主表和失败条件，再进入方法公式。近三届扫描覆盖、后续候选及官方状态见[本轮核验](../reading-notes/research-atlas-20261003.md)。
