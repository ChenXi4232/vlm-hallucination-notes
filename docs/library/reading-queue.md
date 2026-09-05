---
title: 待读与待整理来源
tags:
  - Reading queue
---

# 待读与待整理来源

这里只保留尚未形成 Deep Paper Note 的来源。PDF 文件不直接提交到公开仓库，避免体积、版权和版本混乱。

| 来源 | 计划类型 | 目标方向 | 状态 |
|---|---|---|---|
| Does Playing it Safe Count as Faithfulness? Reassessing LVLM Hallucination Mitigation Methods (arXiv:2609.01888 v1) | 高优先级评测审计 | Evaluation / Recall Trade-off | 暂停收录：摘要称 4 个 benchmarks，正文主协议称 3 个，公开代码仓库又列 CHAIR/AMBER/MMHal/MMStar；待版本澄清 |
| VisER: Visual Evidence and Reliance for Object Hallucination Detection in LVLMs (arXiv:2608.30480 v1) | 候选检测论文 | Token / Logit | 待读：需核对双轴证据是否独立于对象词表与标注 |
| ReWEIGH the Evidence: Calibrating Token-Level Ordinal Visual Evidence to Mitigate Hallucinations in Large Vision-Language Models (arXiv:2608.19075 v1) | 候选方法论文 | Token / Logit | 待读：与 SADT/PatchGate 的增量和代码状态待核对 |
| Targeting the Attention Heads Behind Object Hallucination in LLaVA (arXiv:2608.24966 v1) | 候选机制/负结果 | Attention Head / Path | 待读：需完整核对 head mining、随机头对照与干预退化证据 |
| LLM Unlearning Should Be Form-Independent | 相邻工作 | Form-independent intervention | 相关性待判断 |

## 本轮已迁移

| 来源 | Deep Paper Note |
|---|---|
| Hallucination-aware Intermediate Representation Edit | [HIRE](../papers/hire-intermediate-representation-edit.md) |
| Hallucination Begins Where Saliency Drops | [Saliency / SGRS / LocoRE](../papers/hallucination-begins-where-saliency-drops.md) |
| Mitigating Object Hallucination via Image-Grounded Guidance | [MARINE](../papers/marine-image-grounded-guidance.md) |
| Dynamic Multimodal Activation Steering | [DMAS](../papers/dynamic-multimodal-activation-steering.md) |

## 进入论文库的条件

- [ ] 核对 title、authors、venue/year、原文链接与当前版本；
- [ ] 明确与 VLM hallucination 主线的相关性，避免只因术语相似而收录；
- [ ] 若进入方法库，补齐 benchmark、baseline、关键 ablation 与官方方法图；
- [ ] 记录资料缺失和不可核验边界。
