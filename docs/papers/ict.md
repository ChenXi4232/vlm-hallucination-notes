---
title: "ICT: Image-Object Cross-Level Trusted Intervention for Mitigating Object Hallucination in Large Vision-Language Models"
description: 通过图像级与对象级对照识别可信注意力头，并在推理时注入视觉激活差分
authors: [Junzhe Chen, Tianshu Zhang, Shiyu Huang, Yuwei Niu, Linfeng Zhang, Lijie Wen, Xuming Hu]
venue: CVPR
year: 2025
resource_type: 方法论文
direction: Attention Head / Path
hallucination_type: [Object hallucination]
method_level: [Attention-head-level, Activation intervention]
training: Offline classifier and direction extraction
status: 已精读
source_status: CVPR 2025 官方论文已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://openaccess.thecvf.com/content/CVPR2025/html/Chen_ICT_Image-Object_Cross-Level_Trusted_Intervention_for_Mitigating_Object_Hallucination_in_CVPR_2025_paper.html
overview_figure: ../assets/images/papers/ict-overview.png
overview_figure_source: Figure 2 from the official CVPR 2025 paper
tags: [ICT, Attention heads, Causal intervention, POPE, CHAIR]
---

# ICT

<div class="paper-meta"><span>CVPR 2025</span><span>Attention Head / Path</span><span>Offline extraction</span><span>已精读</span></div>

[论文原文](https://openaccess.thecvf.com/content/CVPR2025/html/Chen_ICT_Image-Object_Cross-Level_Trusted_Intervention_for_Mitigating_Object_Hallucination_in_CVPR_2025_paper.html){ .kb-button .primary }

<div class="paper-tldr"><strong>一句话总结</strong><p>ICT 分别用真实图像对空白/破坏图像、真实对象对不可信对象构造两级判别信号，定位更能表达视觉真实性的 attention heads，再把真实—不可信条件的激活差注入这些头。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/ict-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/ict-overview.png" alt="ICT 官方方法总览"></a><figcaption>官方方法概览图（论文 Figure 2）：image-level/object-level 可信头定位与推理时干预。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 核心假设 | 部分注意力头能稳定区分真实视觉证据与不可信条件 |
| 定位 | 训练轻量分类器评估各头对 image-level、object-level 真值的可分性 |
| 干预 | 选择 top-K 头，将真实/不可信条件的平均 activation shift 按强度注入 |
| 部署 | 单次正常 forward 内修改头输出，不需要每 token 的对比图像分支 |
| 评测 | POPE、CHAIR/MME 与跨模型 shift transfer、时间成本 |

## 2. 研究背景

全层 contrastive decoding 通常需要额外 forward，并把所有头视为同等重要；全局 steering 又容易把对象语义与真假信号纠缠。ICT 的出发点是先找“可信头”，再局部干预。image-level 信号回答模型是否接收到有效图像，object-level 信号回答具体对象陈述是否受视觉支持，两级结合试图减少只学到画面风格或语言频率的头。

不过“分类可分”并不自动等于“因果必要”。头选择器可能利用数据集、prompt 或破坏方式捷径；激活注入的改善也可能来自一般 yes/no bias。跨模型 shift transfer 与随机头对照因此尤其重要。

## 3. 方法详解

离线阶段采集真实图、空白/腐蚀图以及对象真/假条件下的 head output，逐头训练或评估可信度分类器。按 image-level 与 object-level 得分选取头集合，并统计可信相对不可信的平均方向。推理时只在这些头上加缩放后的 shift，再通过原 residual path 影响 logits。

方法把定位与干预分离：定位可以昂贵，但部署不再运行腐蚀图分支。关键超参是 top-K、注入系数和层/头聚合方式。要判定机制性，必须比较同数量随机头、只 image-level、只 object-level、头置换和跨数据重估。

## 4. 实验设计

### 4.1 设置

在 LLaVA 与 Qwen 系列上测试 POPE 的 random/popular/adversarial 子集，并与 VCD、OPERA 等方法比较。时间实验按生成 20/50/80 token 计时；跨模型实验把 LLaVA 提取的 shift 直接用于 Qwen，以检查方向是否仅适配单一模型。

### 4.2 主结果

| 设置 | Regular | ICT | 解读 | 来源 |
|---|---:|---:|---|---|
| Qwen，GQA Popular Acc/F1 ↑ | 75.99 / 74.84 | 81.50 / 80.10 | 两项约 +5 pt | Table 1/3 |
| Qwen，GQA Adversarial Acc/F1 ↑ | 75.46 / 74.33 | 79.73 / 78.68 | 困难负例仍改善 | Table 3 |
| 跨模型 LLaVA shift→Qwen，GQA Random Acc/F1 ↑ | 80.97 / 79.01 | 85.10 / 83.27 | 存在方向迁移 | Table 3 |
| LLaVA 生成 20/50/80 tokens，ms | 405.3/934.6/1440.0 | 415.9/931.9/1485.5 | 接近 1× forward 成本 | Table 2 |
| VCD 相对成本 | 约 2.1–2.4× | ICT 约 1× | 局部注入更高效 | Table 2 |

表中跨模型迁移是 ICT 最有说服力的分析之一：即使 shift 来自另一 backbone，仍优于随机干预。不过主要数值集中在 POPE 式封闭问答，不能直接推出自由描述中同样有效。

### 4.3 消融与分析实验

论文比较图像级、对象级以及联合选择，联合方案整体最佳；随机选择相同数量头明显较弱，说明收益不只是增加 residual norm。top-K 和注入强度存在中间最优区间，过强会破坏一般能力。Table 3 的 LLaVA→Qwen transfer 表明方向含一定可迁移视觉真实性结构；Table 2 则验证无需额外前向的效率优势。仍缺 activation patching 的必要性/充分性闭环，也未对选择数据与测试对象类别的泄漏做最严格隔离。

## 5. 亮点与贡献

- 同时建模全局图像可靠性和局部对象真实性。
- 把昂贵的对照收集留在离线阶段，部署近似单 pass。
- 提供跨模型迁移与时间成本，而不只报精度。

## 6. 局限

头分类得分可能不等于因果贡献；真假对象构造与 corruption 选择会决定方向。POPE 的 yes/no prior 容易被 logit bias 改善，开放生成证据相对不足。跨架构 head 数和维度的映射需额外假设。离线分类器、数据和方向提取不应被称为完全 training-free。

## 7. 与我的研究关系

ICT 可作为“probe 能否安全转成 policy”的强 baseline。实验应分开验证 decodability、局部 patching 效果和自由生成 utility，并使用独立数据选择头、调强度、做最终测试，避免 probe-to-policy 的选择偏差。

## 8. 可执行的后续实验

1. 比较 top-K、随机 K、score-matched 非目标头与 layer-matched 头。
2. 以对象删除/匹配 sham 做 target 与 non-target logit 差分。
3. 在 THRONE/CHAIR 上联合报告 Recall、长度、EOS 和重复率。
4. 选择头、估计方向、调系数、最终测试使用四个独立 split。

## 9. 复现清单

- [x] 官方 Figure 2、主结果、迁移与延迟表已登记
- [ ] 固定 corruption、分类器和 head ranking seed
- [ ] 保存每头 AUROC、方向 norm 和层分布
- [ ] 加入随机头与等层对照
- [ ] 在自由生成上验证并报告 CI

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | image/object 两级可信定位 |
| 机制证据 | 3/5 | 有随机与迁移分析，因果闭环仍有限 |
| 效率 | 5/5 | 推理接近单 forward |
| 相关性 | 5/5 | 连接 head probe 与局部 intervention |

## 11. 来源边界

本文依据 CVPR 2025 官方论文整理。数值来自原文 Tables 1–3；对 probe-to-policy、数据分割和对象删除控制的建议属于本站分析。
