---
title: "DiVE: Decoupling Intra-layer Visual Evidence for Mitigating Hallucinations in Large Vision-Language Models"
description: 在单次前向内定位视觉证据层、构造语言先验参考并进行对比解码
authors: [Xinwei Li, Li Lin, Hui Jiao, Li Yao, Tien-Tsin Wong, Hanqian Wu]
venue: ACL
year: 2026
resource_type: 方法论文
direction: Token / Logit
hallucination_type: [Object hallucination, Attribute hallucination]
method_level: [Intra-layer evidence, Contrastive decoding]
training: Training-free inference
status: 已精读
source_status: ACL 2026 Anthology 官方论文已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://aclanthology.org/2026.acl-long.1742/
overview_figure: ../assets/images/papers/dive-overview.png
overview_figure_source: Figure 2 from the official ACL 2026 paper
tags: [DiVE, Visual evidence, Contrastive decoding, Single forward, ACL]
---

# DiVE

<div class="paper-meta"><span>ACL 2026</span><span>Token / Logit</span><span>Training-free</span><span>已精读</span></div>

[论文原文](https://aclanthology.org/2026.acl-long.1742/){ .kb-button .primary }

<div class="paper-tldr"><strong>一句话总结</strong><p>DiVE 在层内估计有效视觉证据，动态选择中间层并抑制该方向以构造语言先验参考分布，再以正常 logits 对参考 logits 做 contrast；无需额外图像扰动或完整第二次前向。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/dive-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/dive-overview.png" alt="DiVE 官方方法总览"></a><figcaption>官方方法概览图（论文 Figure 2）：视觉证据层识别、层内 decoupling、语言先验参考与对比输出。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 问题 | 无图/噪声对比分支既昂贵又把视觉损坏伪迹混入参考分布 |
| 层选择 | 以 V-LAC 类视觉证据质量分数动态保留中间有效层 |
| 参考构造 | 在选中层从 hidden state 减去视觉证据方向，得到 language-prior-like reference |
| 输出 | 正常 logits 与参考 logits 对比，并以置信阈值过滤候选 |
| 成本 | 单一主 forward 内增加层内计算；无外部图像扰动 |

## 2. 研究背景

VCD/M3ID 等方法通过无图或扰动图得到语言先验分支，再与原图 logits 对比。这能增强视觉依赖，却需要额外 forward，且“损坏图像”同时改变不确定性、语义和 token 分布。DiVE 试图从同一次正常计算内部把视觉证据与文本上下文分开，构造更干净的参考。

核心反直觉点是先抑制视觉证据来获得参考，而不是直接把视觉方向加倍。若视觉方向估计准确，正常分布减参考分布能突出视觉支持 token；若估计混入语义或 residual scale，contrast 也会放大错误。

## 3. 方法详解

DiVE 计算每层 attention 中视觉 token 对当前预测的有效贡献，排除最早和最晚各 $\kappa L$ 层，再以动态阈值选择证据层。对选中层聚合视觉 value/attention 形成方向，从 hidden state 以强度 $\gamma$ 减去，得到视觉受抑制表示及参考 logits。

最终用原始 logits 对该 reference 做 contrastive calibration，并仅对置信候选应用，避免低概率词被无界放大。方法不需要训练或外部模型，但 $\kappa$、$\gamma$、置信阈值仍需校准；不同任务阈值差异较大。

## 4. 实验设计

### 4.1 设置

主干为 Qwen2.5-VL-7B 与 LLaVA-v1.5-7B，扩展到 LLaVA-13B/Qwen-VL。评测 POPE 的 MS-COCO/A-OKVQA/GQA 三种采样、CHAIR 与 MME-Hallucination，baseline 包括 VCD、M3ID、SID、ONLY、AVISC。另报告延迟与显存。

### 4.2 主结果

| 设置 / 指标 | Base | DiVE | 解读 | 来源 |
|---|---:|---:|---|---|
| Qwen，POPE MS-COCO Avg Acc/F1 ↑ | 83.71 / 80.86 | 87.66 / 86.47 | +3.95 / +5.61 | Table 1 |
| Qwen，POPE GQA Avg Acc/F1 ↑ | 83.33 / 82.84 | 85.56 / 85.55 | 困难分布一致提升 | Table 1 |
| LLaVA，A-OKVQA Avg Acc/F1 ↑ | 78.32 / 81.86 | 85.98 / 86.22 | 提升显著 | Table 2 |
| Qwen CHAIR$_S$/$_I$ ↓，Recall ↑ | 37.6 / 9.3；71.7 | 31.4 / 7.3；73.0 | 幻觉降且 Recall 升 | Table 4 |
| LLaVA CHAIR$_S$/$_I$ ↓，Recall ↑ | 53.2 / 14.7；80.5 | 47.4 / 13.0；81.5 | 未靠少生成 | Table 4 |
| MME-Hall Qwen / LLaVA ↑ | 690.0 / 643.3 | 720.0 / 671.7 | 对象和属性均提升 | Table 3 |

CHAIR 与 Recall 同时改善是最重要的自由生成证据。POPE 某些子集 F1 改善大于 accuracy，说明类别阈值和 precision/recall 结构仍应逐项查看，不能只报平均。

### 4.3 消融与分析实验

排除比例 $\kappa=0.05$ 在两主干上最好：Qwen POPE Acc/F1 86.70/86.38、CHAIR 31.4/7.3、MME 720；过小或过大均退化。$\gamma=0.5$ 最佳，过强抑制会扭曲语义。层选择消融中，仅用 visual attention ratio 得 CHAIR$_S$ 36.2，乘 V-LAC 为 33.6，单最佳层 MME 688.3，完整 DiVE 为 31.4/720，说明“注意得多”不等于证据质量且证据跨层分布。直接 vision boost 在 Qwen 仅 84.01/82.91、CHAIR 34.6/8.3，弱于 DiVE 86.70/86.38、31.4/7.3，支持“构造参考再对比”而非简单增强。成本表约 1.03× FLOPs、1.28× token latency，需按真实硬件理解。

## 5. 亮点与贡献

- 从正常 forward 内部构造参考，避免破坏图像的外部分支。
- 对层选择、抑制强度、直接 boost 都有针对性消融。
- CHAIR 同时报 Recall，且给出延迟/显存而非只称高效。

## 6. 局限

层内方向不一定是纯视觉证据，可能混入对象语义和位置偏差。POPE/CHAIR 仍以对象存在性为主，细粒度空间与遮挡场景是论文承认的难点。任务间 confidence threshold 差异大，部署需校准。1.28× token latency 不是零开销，且 GPU/实现相关。

## 7. 与我的研究关系

DiVE 是单 pass 内部反事实的强 baseline：其 reference construction 可与真实无图/对象删除分支逐 token 对齐，检验内部抑制是否真的近似语言先验。还可把证据质量分数用于风险门控，而非全词统一 contrast。

## 8. 可执行的后续实验

1. 比较 DiVE reference 与 no-image/blank/object-removed logits 的 KL 和 token 排名。
2. 用 matched sham 检查视觉方向对非目标对象的副作用。
3. 在等 latency 下比较 VCD、单层 DiVE、完整 DiVE。
4. 记录逐 token 触发、Recall、长度、EOS、重复与 target logit 恢复。

## 9. 复现清单

- [x] 官方 Figure 2、主表、层选择/强度/boost/成本分析已登记
- [ ] 固定 $\kappa$、$\gamma$、阈值选择 split
- [ ] 保存逐层 V-LAC、视觉方向与参考 logits
- [ ] 在统一硬件重测 latency/FLOPs/显存
- [ ] 补多 seed 或图片 bootstrap CI

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 层内 decoupling 构造对比参考 |
| 机制证据 | 4/5 | 多个替代解释被针对性消融 |
| 效率 | 4/5 | 比双 forward 低，但仍有 1.28× 延迟 |
| 相关性 | 5/5 | 直接连接证据层与单 pass 干预 |

## 11. 来源边界

本文依据 ACL 2026 Anthology 官方论文整理。数字来自 Tables 1–9 与成本表；对 no-image reference 对齐、matched sham 和风险门控的建议属于本站分析。
