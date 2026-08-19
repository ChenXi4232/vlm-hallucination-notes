---
title: Understanding and Mitigating Hallucination in Large Vision-Language Models via Modular Attribution and Intervention
description: 通过模块级归因和组件消融定位 hallucination heads，并进行定向注意力干预
authors:
  - Tianyun Yang
  - Ziniu Li
  - Juan Cao
  - Chang Xu
venue: ICLR
year: 2025
resource_type: 方法论文
direction: Attention Head / Path
hallucination_type:
  - Object hallucination
method_level:
  - Module-level
  - Head-level
training: Inference-time / optional fine-tuning
status: 已精读
source_status: ICLR 元数据已核对；知识卡解读待持续复核
paper_url: https://openreview.net/forum?id=Bjq4W7P2Us
tags:
  - Object hallucination
  - Modular attribution
  - Attention head
  - Causal intervention
  - CHAIR
  - Nocaps
---

# Understanding and Mitigating Hallucination in Large Vision-Language Models via Modular Attribution and Intervention

<div class="paper-meta"><span>ICLR 2025</span><span>方法论文</span><span>Module / Head</span><span>Inference-time</span><span>已精读</span></div>

[OpenReview](https://openreview.net/forum?id=Bjq4W7P2Us){ .kb-button } [ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/8001c3568152d134d821cd46d4d84768-Abstract-Conference.html){ .kb-button }

## 核心问题

这篇论文关注 LVLM 在开放式图像描述中的 **object hallucination**：模型生成图像中不存在的物体。与只在输出层做 decoding 修正的方法不同，论文试图回答“幻觉由模型内部哪些模块 causally 触发”。其核心发现是：hallucination 并非均匀来自所有层或所有模块，而是与少量 attention heads 强相关。这些 heads 通常位于中后层，对 hallucination tokens 的概率提升更明显，并且相比视觉 token 更依赖文本上下文，表现出较强的 language-prior / text-dominant 行为。

## 方法一句话概括

论文先用 modular attribution / counterfactual head ablation 计算每个 MLP、MHA 与 attention head 对 hallucination token probability 的贡献，再定位 hallucination heads，并通过 AD-HH 在推理时动态抑制这些 heads 对 text tokens 的 attention，或通过 TF-HH 只微调这些 heads 来缓解幻觉。

## benchmark / metric

主要实验基于 COCO captioning，使用 CHAIRs 与 CHAIRi 衡量 object hallucination；同时在 Nocaps 上测试 out-of-domain 泛化，在 MM-Vet、MME 与 human evaluation 中检查通用多模态能力和生成质量。baseline 包括 Greedy、DoLA、VCD、OPERA、LURE、HALC 等。论文报告 AD-HH 在 LLaVA-7B 上能显著降低 COCO 的 CHAIRs / CHAIRi，并且不明显牺牲 BLEU、ROUGE、METEOR 或 MM-Vet 表现。

## 与我研究的关系

这篇论文与我的 token-level / head-level / logit-level 视觉依赖研究高度相关。它的 attribution score 本质上是组件级反事实：比较原模型与移除某组件后 hallucination token 概率的变化。我的真实图像 vs 空白图像实验可以将其扩展为 image counterfactual：比较 hallucination heads 与 non-hallucination heads 在真实图像、空白图像或反事实图像下的 logit 差异、head output 差异和 attention-to-image ratio。如果 hallucination heads 在图像替换后变化更小，同时 text attention 更高，就能支持“幻觉来自语言先验支配或视觉依赖不足”的假设。它也可以和我的 VR、PD、RBC 指标结合，用于验证高 hallucination-influence heads 是否对应低 visual dependence。

## 是否适合作为 baseline

非常适合作为 baseline，尤其是 **head-level intervention baseline**。AD-HH 是 inference-time 方法，不需要 object detector、外部 LLM evaluator 或额外训练，适合低算力复现；TF-HH 可作为轻量 training-time baseline。但需要注意，AD-HH 依赖显式 attention weights，可能影响 FlashAttention 等高效实现；另外，hallucination head set 可能依赖 COCO / CHAIR 的 object-level 标注，迁移到 attribute、relation 或 VQA 场景时需要重新验证。

## 未来可做的 follow-up experiment

1. **Hallucination heads 的视觉依赖验证**：在 LLaVA-v1.5-7B 上比较真实图像与空白图像下每个 head 的 output norm difference、image attention ratio 与 token-level Δlogit，检验 hallucination heads 是否更不受视觉输入影响。

2. **AD-HH 与 logit-level 方法组合**：比较 Greedy、AD-HH、M3ID、OPERA、SID 与 AD-HH+M3ID，观察 head-level text-attention suppression 与 logit-level visual amplification 是否互补。

3. **幻觉发生前的 head dynamics**：对 CHAIR 标注出的 hallucinated object token，追踪其前 5 个 decoding steps 中 hallucination heads 的 text attention、image attention 和候选 token rank，判断幻觉是否在 token 选择前已经表现为 text-prior 增强。

4. **跨幻觉类型泛化**：在 Visual Genome / SHR-style benchmark 上测试 AD-HH 是否也能降低 attribute、relation、counting hallucination。如果只对 object hallucination 有效，则说明其机制可能受 COCO object label 与 CHAIR 指标限制。
