---
title: Multi-Modal Hallucination Control by Visual Information Grounding
description: 以视觉条件分布与语言先验分布的差异缓解生成中的 conditioning dilution
authors:
  - Alessandro Favero
  - Luca Zancato
  - Matthew Trager
  - Siddharth Choudhary
  - Pramuditha Perera
  - Alessandro Achille
  - Ashwin Swaminathan
  - Stefano Soatto
venue: CVPR
year: 2024
resource_type: 方法论文
direction: Token / Logit
hallucination_type:
  - Object hallucination
method_level:
  - Logit-level
  - Decoding
training: Training-free
status: 已精读
source_status: 原文元数据已核对；知识卡解读待持续复核
paper_url: https://arxiv.org/abs/2403.14003
tags:
  - Object hallucination
  - Logit-level
  - Contrastive decoding
  - Language prior
  - Training-free
  - CHAIR
  - POPE
---

# Multi-Modal Hallucination Control by Visual Information Grounding

<div class="paper-meta"><span>CVPR 2024</span><span>方法论文</span><span>Token / Logit</span><span>Training-free</span><span>已精读</span></div>

[论文原文](https://arxiv.org/abs/2403.14003){ .kb-button } [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2024/html/Favero_Multi-Modal_Hallucination_Control_by_Visual_Information_Grounding_CVPR_2024_paper.html){ .kb-button }

## 核心问题

这篇论文研究 VLM 在图像描述和视觉问答中的 **object hallucination**：模型生成或确认图像中并不存在的对象。作者认为，这类幻觉并不主要来自视觉编码器完全无法理解图像，而是来自生成过程中对 **language prior** 的过度依赖。随着 autoregressive generation 进行，视觉输入对后续 token 的影响逐渐减弱，模型越来越依赖已经生成的文本上下文和语言先验，形成 **conditioning dilution / fading memory effect**，因此靠后的 object token 更容易出现 hallucination。

## 方法一句话概括

论文提出 **PDM（Prompt Dependency Measure）** 衡量 next-token distribution 对视觉输入的依赖程度，并提出 **M3ID（Multi-Modal Mutual Information Decoding）**，在解码时放大有图像分布与无图像分布的差异，即增强 \(l_c-l_u\)，使生成 token 更依赖视觉输入而非语言先验。

## Benchmark / Metric

实验主要使用 **MS COCO** 和 **POPE**。在 captioning 任务中，使用 COCO 标注评估对象幻觉，指标包括 **CHAIRi**、**CHAIRs** 和 **Cover**。CHAIRi 衡量生成对象中幻觉对象比例，CHAIRs 衡量包含至少一个幻觉对象的 caption 比例，Cover 衡量 caption 覆盖真实对象的程度，避免模型通过生成短 caption 降低幻觉率。在 VQA 任务中，使用 **POPE**，将 hallucination 转化为 “Is a <object> present in the image?” 的 Yes/No 判断，指标包括 accuracy 和 Yes ratio。

## 与我研究的关系

这篇论文与我的 token-level / logit-level 反事实实验高度相关。它本质上比较 **with-image distribution** 与 **without-image distribution**，这与真实图像 vs 空白图像 / 反事实图像下的 logits 差异分析非常接近。PDM 可视为 distribution-level visual dependency metric，而我的 VR、PD、RBC 可以进一步细化到具体 token 的 logit、probability 和 rank 变化。论文提出的 conditioning dilution 也能支持我研究生成过程中视觉依赖是否随 token position、layer 或 attention head 衰减。

## 是否适合作为 Baseline

这篇论文非常适合作为 related work 和 baseline。M3ID 是 inference-time 方法，不需要 object detector，也不依赖 GPT evaluator，只需要获得有图像和无图像条件下的 logits，适合低算力复现。它可作为 decoding-level mitigation baseline，也可作为 PDM 与我的 VR / PD / RBC 指标对比的 conceptual baseline。但它不应作为唯一 baseline，因为 PDM 衡量的是 visual dependency，不等价于 hallucination correctness；无图像输入也可能引入 prompt-format confound；并且实验主要覆盖 object hallucination，不能充分解释 attribute、relation、counting 或 reasoning hallucination。

## 未来可做的 Follow-up Experiment

1. 比较 hallucinated object token 与 grounded object token 的 real-image vs blank-image logit gap、probability gap 和 rank change，验证幻觉 token 是否更少依赖视觉输入。
2. 在同一批 token 上计算 PDM、VR、PD、RBC，分析 distribution-level 与 token-level visual dependency 指标的一致性和差异。
3. 记录不同 layer/head 对 image tokens 的 attention mass，分析 conditioning dilution 是否对应 head-level 视觉注意力下降。
4. 比较 no-image、blank-image、noise-image、mismatched-image 条件下的 logits，检验 unconditioned distribution 是否真的代表 language prior。
5. 借鉴 M3ID，用 \(l_{real}-l_{blank}\) 或 \(l_{real}-l_{counterfactual}\) 设计 Visual Dependency Decoding，作为新的低算力 hallucination mitigation baseline。

---

**来源状态**：论文元数据与原文入口已核对；本页方法解读来自个人知识卡，引用具体结果前仍应回查原文表格。
