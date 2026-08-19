---
title: Surveys
description: VLM hallucination 综述、专题脉络与证据缺口
---

# Surveys

Survey 页面不是论文列表，而是跨论文形成的结构化判断。每篇专题综述应区分：已被多篇工作支持的结论、尚有冲突的证据，以及可执行的开放问题。

## 计划中的专题

| 专题 | 核心问题 | 当前入口 |
|---|---|---|
| Hallucination taxonomy | object、attribute、relation、reasoning 与 long-form 如何区分 | [研究版图](../research-map.md) |
| Attention / head intervention | 视觉敏感头、语言先验头与路径干预的证据是否一致 | [Head / Path](../directions/attention-heads.md) |
| Logit-level mitigation | contrastive decoding 是否真正增加视觉 grounding | [Token / Logit](../directions/token-logit.md) |
| Representation editing | residual、MLP、KV 和 activation steering 的关系 | [Representation](../directions/representation.md) |
| Evaluation trade-off | 幻觉下降是否以 recall、coverage 或生成质量为代价 | [Evaluation](../directions/evaluation.md) |

!!! info "发布规则"
    这里只发布已经整理、可回溯到公开论文的综合判断。未成熟研究判断保留在私有实验仓库。
