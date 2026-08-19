---
title: Cracking the Code of Hallucination in LVLMs with Vision-aware Head Divergence
description: 以有图和无图条件下的 head-output divergence 识别 vision-aware heads 并进行强化
authors:
  - Jinghan He
  - Kuan Zhu
  - Haiyun Guo
  - Junfeng Fang
  - Zhenglin Hua
  - Yuheng Jia
  - Ming Tang
  - Tat-Seng Chua
  - Jinqiao Wang
venue: ACL
year: 2025
resource_type: 方法论文
direction: Attention Head / Path
hallucination_type:
  - Object hallucination
method_level:
  - Head-level
training: Training-free
status: 已精读
source_status: ACL Anthology 与代码元数据已核对；知识卡解读待持续复核
paper_url: https://aclanthology.org/2025.acl-long.175/
code_url: https://github.com/jinghan1he/VHR
tags:
  - Object hallucination
  - Vision-aware head
  - Head divergence
  - Training-free
  - CHAIR
  - POPE
---

# Cracking the Code of Hallucination in LVLMs with Vision-aware Head Divergence：知识库条目

<div class="paper-meta"><span>ACL 2025 Long</span><span>方法论文</span><span>Head-level</span><span>Training-free</span><span>已精读</span></div>

[ACL Anthology](https://aclanthology.org/2025.acl-long.175/){ .kb-button } [官方代码](https://github.com/jinghan1he/VHR){ .kb-button }

## 核心问题

本文关注 LVLM 在图像描述与视觉问答中生成与图像不一致内容的问题，尤其是 object hallucination。论文的核心问题不是简单判断模型是否“看图”，而是进一步追问：在 Transformer 内部，是否存在一部分 attention heads 负责视觉信息注入？当这些 heads 的作用不足时，模型是否更容易被语言先验主导并产生幻觉？因此，该工作将 hallucination 从输出层错误推进到 head-level visual dependence 的机制分析。

## 方法一句话概括

论文提出 Vision-aware Head Divergence（VHD），通过比较同一 head 在有图像输入与无图像输入条件下的输出差异来识别 vision-aware heads，并进一步提出 Vision-aware Head Reinforcement（VHR），在推理时放大这些 heads 的输出以增强视觉 grounding、降低 hallucination。

## benchmark / metric

实验主要使用 CHAIR、POPE 和 LLaVA-Bench-in-the-Wild。CHAIR 用于评估 caption 中提到的物体是否出现在图像标注中，适合衡量 object hallucination；POPE 将物体存在性转化为 yes/no 问答，包含 random、popular、adversarial 设置；LLaVA-Bench 结合 GPT-4o 评价回答的 accuracy、detailedness 和 naturalness。模型包括 InstructBLIP-7B、LLaVA-1.5-7B 和 LLaVA-NeXT-7B，baseline 包括 Greedy、Beam、DoLa、VCD、OPERA、CODE 和 EAH。整体结果显示 VHR 在 CHAIR 上提升明显，在 POPE 上提升较小但较稳定。

## 与我研究的关系

本文与我的 token-level / head-level / logit-level 反事实研究高度相关。VHD 本质上是 head-output 层面的“真实图像 vs 无图像”差异度量，可作为我当前 VR、PD、RBC 等 logits-level 视觉依赖指标的中间层 counterpart。若某 token 的 logits gap 低且 T-VHD 也低，说明该 token 更可能由语言先验驱动；若 logits gap 高但仍 hallucinate，则可能表示模型确实使用了视觉信号，但视觉-语言对齐或证据选择出现错误。该文还提醒我，attention weight 本身可能不足以解释视觉依赖，head output divergence 更接近可干预的机制变量。

## 是否适合作为 baseline

适合作为高优先级 analysis baseline 和中高优先级 mitigation baseline。优点是无需训练、不依赖 object detector 或外部 LLM，且与 head-level intervention 直接相关；缺点是需要修改模型 forward 或 hook 每个 attention head 的输出，对不同 LVLM 架构适配成本较高。若后续实验使用 LLaVA-1.5，VHD/T-VHD 很适合作为视觉依赖指标对照；VHR 则可作为 head-level 干预方法，与 M3ID、SID、OPERA、DLC 等 decoding-level 方法形成横向比较。

## 未来可做的 follow-up experiment

1. 比较 VR 与 T-VHD 的 token-level 相关性：在 COCO caption 中记录每个 token 的真实图像 vs 空白图像 logits gap、T-VHD 和 hallucination 标签，检验 hallucinated object tokens 是否同时表现为低 logits visual dependence 与低 head-level visual dependence。

2. 做 high-VHD head suppression / reinforcement：对 VHD 排名前列的 heads 分别设置 alpha 小于 1 与大于 1，观察 CHAIR、POPE、object logits 和输出长度变化，以验证 vision-aware heads 是否具有因果作用。

3. 分析 hallucination onset 前的视觉依赖轨迹：选取产生幻觉的长 caption，比较 hallucinated token 前若干步与正确 object token 前若干步的 T-VHD、VR、entropy 和 top-k logits，判断幻觉是否伴随视觉依赖提前塌缩。

4. 检验 VHR 是否真正提升视觉依赖：比较 baseline 与 VHR 下 correct object token 和 hallucinated object token 的 logits gap。如果 CHAIR 降低但 VR/T-VHD 未提升，则可能说明 VHR 只是改变生成风格或长度，而非真正增强视觉 grounding。
