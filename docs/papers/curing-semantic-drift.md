---
title: "Curing Semantic Drift: A Dynamic Approach to Grounding Generation in Large Vision-Language Models"
description: 用外部视觉对齐分数动态校准 top-k token，处理长生成中的 semantic drift
authors:
  - Jiahe Chen
  - Jiaying He
  - Qiyuan Chen
  - Qian Shao
  - Jiahe Ying
  - Hongxia Xu
  - Jintai Chen
  - Jianwei Zheng
  - Jian Wu
venue: arXiv
year: 2025
resource_type: 方法论文
direction: Long-form / Semantic Drift
hallucination_type:
  - Object hallucination
  - Long-form hallucination
method_level:
  - Token-level
  - Logit-level
training: Training-free
status: 已精读
source_status: arXiv 元数据已核对；版本持续更新
paper_url: https://arxiv.org/abs/2506.21509
tags:
  - Semantic drift
  - Long-form generation
  - Logit calibration
  - CLIP
  - Training-free
  - CHAIR
  - POPE
---

# Curing Semantic Drift: A Dynamic Approach to Grounding Generation in LVLMs｜知识库条目

<div class="paper-meta"><span>arXiv 2025</span><span>方法论文</span><span>Long-form / Logit</span><span>Training-free</span><span>已精读</span></div>

[论文原文](https://arxiv.org/abs/2506.21509){ .kb-button }

## 核心问题

这篇论文关注 LVLM 在长文本生成中的 **semantic drift**：随着 autoregressive decoding 推进，模型输出逐渐脱离输入图像，越来越受 linguistic priors 支配，最终产生 plausible but visually unfaithful 的 hallucination。作者特别强调，幻觉并不总是因为模型完全“看不到”正确视觉信息，而常常是 **token selection failure**：在某些关键解码步，top-k candidates 中已经存在更视觉忠实的候选 token，但模型仍选择了 raw logits 更高、语言上更顺滑但视觉上错误的 token。因此，该工作将 hallucination 从最终文本错误重新定义为一种动态的、token-level generation trajectory failure。

## 方法一句话概括

论文提出 **Dynamic Logits Calibration (DLC)**：一种 training-free decoding 方法，在每个生成步用 CLIP / SigLIP / FG-CLIP 作为 lightweight visual referee，对 top-k candidate tokens 计算 intrinsic visual relevance 与 contextual visual coherence，并根据历史视觉一致性基线动态校准 logits，使视觉 grounded 的候选 token 更容易被选中。

具体而言，DLC 维护一个历史视觉基线 \(\bar{B}_t\)，用最近窗口文本与图像的 CLIP score 表示当前生成轨迹的视觉一致性。对每个候选 token，方法计算两类分数：一是 **CCTA**，即“当前上下文 + candidate token”与图像的对齐程度；二是 **ITA**，即 candidate token 单独与图像的视觉相关性。二者平均得到综合视觉分数，再与历史基线比较得到 **RVA**，最后通过乘性方式修正原始 logits。该方法不需要训练，不需要 object detector，但依赖外部视觉-文本对齐模型。

## benchmark / metric

实验覆盖 LLaVA-1.5、InstructBLIP、MiniGPT-4，主要为 7B 模型，并扩展到部分 13B 模型。benchmark 包括：MS-COCO 上的 **CHAIRs / CHAIRi**，用于评估 caption 中的 object hallucination；**POPE** random / popular / adversarial，用于 yes/no object existence hallucination；**SHR**，用于更细粒度的 sentence-level 与 word-level hallucination；**GPT-4o assisted evaluation**，评估 correctness 与 detailedness；以及 **MME**，检查 hallucination mitigation 是否损害 general multimodal ability。baseline 包括 Nucleus Sampling、VCD、ICD、SID、OPERA。结果显示 DLC 在长文本 512-token 设置下优势更明显，说明 semantic drift 假设主要适用于长生成场景。

## 与我研究的关系

这篇论文与我的 token-level / logit-level 视觉依赖研究高度相关。它提供了一个直接可复用的分析视角：不要只判断最终回答是否 hallucinate，而要检查每个生成步中 raw logits、visual alignment score 和 top-k candidate ranking 的冲突。对我的真实图像 vs 空白图像反事实实验而言，DLC 可作为外部视觉依赖 proxy：我可以比较 selected token 的 real-image logits、blank-image logits 与 CLIP-based CCTA / ITA 是否一致。如果幻觉 token 在真实图像和空白图像下 logit 差异很小，同时 CLIP visual score 低，但 raw logit 高，则可以更强地支持 “LLM prior dominance / selection failure” 假设。它也启发 head-level 分析：在 CCTA 或 VR 指标突然下降的 token step，是否存在特定 layer/head 对 image tokens 的 attention collapse。

## 是否适合作为 baseline

适合作为高优先级 baseline。优点是 training-free、token-level、logit-level、低算力可复现，并且不需要额外标注或 object detector；与 VCD、SID、OPERA、M3ID 可以共同构成 decoding-time hallucination mitigation baseline 组。限制是它依赖 CLIP/SigLIP 作为外部评估器，因此不能证明 LVLM 内部真的依赖视觉输入；CLIP 对单 token、数量、空间关系、否定和细粒度属性的可靠性也有限。此外，CHAIR 降低可能部分来自更保守或更短的输出，因此复现时应同时报告 caption length、coverage / recall 与 detailedness。

## 未来可做的 follow-up experiment

1. **CCTA vs VR 同步性实验**：在 LLaVA-1.5 上生成 COCO 长 caption，记录每步 CCTA、ITA、真实图像 logits、空白图像 logits 和 hallucination label，检验外部 CLIP drift 是否与内部 visual reliance drop 同步。

2. **selection failure 统计实验**：对 hallucination token 的 top-k candidates 计算 raw logit rank、VR rank、CCTA / ITA rank，统计是否存在“视觉依赖更高但未被选择”的候选 token，用于区分 candidate absence 与 selection failure。

3. **head-level drift onset 实验**：以 hallucination onset 为中心窗口，记录各 layer/head 对 image tokens 的 attention mass、entropy 和 rollout contribution，观察视觉注意力下降是否先于 logit-level drift。

4. **DLC vs M3ID vs VR-guided decoding**：比较外部 CLIP-guided calibration、unconditioned-prior contrast 和真实/空白图像 logits calibration 在 CHAIR、POPE、coverage、caption length 上的差异，评估哪类视觉依赖信号最适合作为我的方法基础。

5. **CLIP proxy 失效分析**：在 POPE adversarial 或高共现物体子集上检查 DLC 是否会奖励“视觉相关但事实错误”的 token，验证外部视觉对齐模型是否会被 co-occurrence prior 误导。

---

**版本提醒**：该预印本存在修订版本。本页引用结论时应记录所读取的 arXiv version，避免把不同版本的实验设置混合。
