---
title: "Intervene-All-Paths: Unified Mitigation of LVLM Hallucinations across Alignment Formats"
description: 识别并联合干预 image-to-input、image-to-output 与 text-to-text 幻觉路径
authors:
  - Jiaye Qian
  - Ge Zheng
  - Yuchen Zhu
  - Sibei Yang
venue: NeurIPS
year: 2025
resource_type: 方法论文
direction: Attention Head / Path
hallucination_type:
  - Object hallucination
  - Multi-format hallucination
method_level:
  - Head-level
  - Causal path
training: Training-free
status: 已精读
source_status: NeurIPS/OpenReview 与代码元数据已核对；知识卡解读待持续复核
paper_url: https://openreview.net/forum?id=HRBhNqkG03
code_url: https://github.com/SooLab/AllPath
tags:
  - Object hallucination
  - Causal path
  - Attention head
  - Training-free
  - CHAIR
  - POPE
  - Recall
---

# Intervene-All-Paths：Unified Mitigation of LVLM Hallucinations across Alignment Formats 知识库条目

<div class="paper-meta"><span>NeurIPS 2025</span><span>方法论文</span><span>Head / Causal Path</span><span>Training-free</span><span>已精读</span></div>

[OpenReview](https://openreview.net/forum?id=HRBhNqkG03){ .kb-button } [官方代码](https://github.com/SooLab/AllPath){ .kb-button }

## 核心问题

这篇论文关注 LVLM 在不同 question–answer alignment formats 下的 hallucination 缓解问题，尤其是 object hallucination 与 visual grounding failure。作者认为，现有方法常只干预单一路径，例如增强 image-to-output-text attention 或抑制 text-dominant heads，因此在 POPE、MCQ-POPE、CHAIR 等不同格式 benchmark 上表现不稳定。论文的核心问题是：LVLM 幻觉是否来自单一路径失效，还是来自 image-to-input-text、image-to-output-text 与 text-to-text 多条 causal pathways 的交互？实验显示，不同任务格式会诱导模型依赖不同路径，因此需要统一的 multi-path head intervention 框架。

## 方法一句话概括

AllPath 先分别识别 text-to-text 与 image-to-text 路径中的 hallucination-relevant attention heads，再对抑制幻觉的 heads 进行增强、对促进幻觉的 heads 进行压制，从而在 inference time 通过多路径 head scaling 缓解 LVLM hallucination。

## benchmark / metric

实验主要使用 LLaVA-1.5-7B，并扩展到 Qwen-VL-Chat、Qwen2.5-VL 等模型。benchmark 包括 POPE、MCQ-POPE、CHAIR 与 MME hallucination subsets。POPE 使用 Accuracy 与 F1 评估 yes/no object existence；MCQ-POPE 使用 Accuracy 与 Macro-F1 评估多选对象判断；CHAIR 使用 CHAIRs 与 CHAIRi 衡量 caption 中 hallucinated objects 的比例；MME 使用 existence、count、position、color 等 hallucination-related 子集。baseline 包括 Vanilla、VCD、ICD、PAI 与 AD-HH。主要结果显示，AllPath 在 POPE、MCQ-POPE 与 CHAIR 上均优于单路径或单类 decoding/intervention 方法，说明多路径联合干预比单独增强视觉路径或压制文本路径更稳定。

## 与我研究的关系

该论文最有价值的部分不是最终性能，而是将 hallucination 拆解到 transformer causal pathways 与 attention heads 的机制层面。它提供了一个可复用的 head-level attribution 框架：T2T heads 通过 modified Log Probability Increase 衡量其对 hallucinated / non-hallucinated tokens 的贡献；I2T heads 通过 object-token 到 image-region 的 attention alignment 衡量视觉 grounding 能力。这为 token-level、head-level、logit-level 的幻觉解释提供了直接参考，也能帮助区分“视觉证据不足”“文本路径过强”与“格式对齐依赖”三类机制。

## 是否适合作为 baseline

适合作为高优先级 baseline，尤其适合与 OPERA、SID、VCD、M3ID、DLC 等 inference-time mitigation 方法对比。它的优势是 training-free、机制解释性强、直接作用于 attention heads，并且跨 QA format 设计。主要复现难点在于 head identification：I2T head probing 需要 object-region alignment 或对象标注，open-ended generation 中 hallucinated / non-hallucinated token 的划分也可能引入标注噪声。因此它既适合作为 baseline，也适合作为被改进的 anchor method。

## 未来可做的 follow-up experiment

一个直接 follow-up 是将 AllPath 的 static head scaling 改造成 dynamic intervention：不再对所有 decoding steps 使用固定 \(\gamma^+\) 与 \(\gamma^-\)，而是根据当前 token 的 path competition、bad-head activation、entity risk 或 visual grounding demand 动态调整干预强度。第二，可以比较 static AllPath 与 Dynamic AllPath 在 CHAIR 长文本生成中的差异，验证 hallucination 是否只在特定 decoding stage 需要强干预。第三，可做 ablation：仅动态增强 I2T heads、仅动态抑制 T2T bad heads、随机 heads 动态干预，以验证效果是否确实来自 AllPath 识别出的 causal heads。第四，可以测试不同 prompt format 下 head set 是否迁移，分析 AllPath 的 format-dependence 是否限制真实场景泛化。
