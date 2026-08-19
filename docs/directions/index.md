---
title: 研究方向总览
---

# 研究方向

| 方向 | 核心问题 | 当前代表卡片 |
|---|---|---|
| [Token / Logit](token-logit.md) | 幻觉 token 是否更少依赖视觉输入？ | M3ID、SID、DLC |
| [Attention Head / Path](attention-heads.md) | 哪些 head/path 写入视觉证据或放大语言先验？ | MAI、VHD/VHR、AllPath |
| [Representation / Activation](representation.md) | 错误语义在哪一层进入 residual stream？ | IR Edit、activation steering（待整理） |
| [Long-form / Drift](long-form.md) | 视觉依赖是否随生成长度持续衰减？ | Curing Semantic Drift、OPERA |
| [Evaluation / Recall](evaluation.md) | 幻觉下降是否只是保守化或内容删除？ | CHAIR、POPE、coverage/recall 审计 |

## 方向选择原则

- 能用同一批样本在 token、head 和 logit 层形成闭环证据。
- 低算力可执行，优先 inference-time 或 teacher-forced analysis。
- 干预结果必须形成 hallucination–recall–quality Pareto 对比。
- 机制主张需要 targeted ablation 或 activation patching 支撑。

