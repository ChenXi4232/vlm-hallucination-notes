---
title: "Mitigating Hallucinations in Large Vision-Language Models via DPO: On-Policy Data Hold the Key"
description: OPA-DPO 用当前策略采样、最小纠错和图像聚焦偏好约束缓解 LVLM 对象幻觉
authors: [Zhihe Yang, Xufang Luo, Dongqi Han, Yunjian Xu, Dongsheng Li]
venue: CVPR
year: 2025
resource_type: 方法论文
direction: Training / Alignment
hallucination_type: [Object hallucination, Free-form generation]
method_level: [Sequence-level, Training-level]
training: LoRA SFT plus DPO
status: 已精读
source_status: CVPR 2025 官方论文、项目页与官方代码已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://arxiv.org/abs/2501.09695
code_url: https://github.com/zhyang2226/OPA-DPO
overview_figure: ../assets/images/papers/opa-dpo-overview.png
overview_figure_source: Figure 3 from the official CVPR 2025 paper
tags: [OPA-DPO, DPO, On-policy, Image focus, CVPR Oral]
---

# OPA-DPO

<div class="paper-meta"><span>CVPR 2025 Oral</span><span>Training / Alignment</span><span>LoRA SFT + DPO</span><span>已精读</span></div>

[论文原文](https://arxiv.org/abs/2501.09695){ .kb-button .primary } [官方代码](https://github.com/zhyang2226/OPA-DPO){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>OPA-DPO 认为离线偏好与待优化策略不匹配是 DPO 缓解幻觉失效的主因：先从当前策略采样真实错误，再用强视觉模型做最小纠错，经过对齐 SFT 后在同一策略分布上做带 anchor 与 image-focus 的 DPO。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/opa-dpo-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/opa-dpo-overview.png" alt="OPA-DPO 官方流程"></a><figcaption>官方方法概览图（论文 Figure 3）：on-policy 采样、最小纠错、LoRA SFT 与偏好优化。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 问题 | 通用偏好数据不覆盖当前 LVLM 自己会犯的视觉错误 |
| 数据 | 当前 policy 生成 rejected response，GPT-4V 最小改正为 chosen response |
| 训练 | ground truth + correction 先 SFT，再从 aligned policy 做 DPO |
| 特殊项 | Anchor loss 防 chosen 概率下降；image-focus 调整视觉 token 贡献 |
| 评测 | AMBER、MMHal-Bench、Object HalBench、POPE 与重复率 |

## 2. 研究背景

DPO 假设偏好对覆盖目标策略的重要错误区域。若负例来自其他模型或人工模板，当前模型可能轻易区分其风格，却没有学习自己容易犯的对象错误。OPA-DPO 把 on-policy 定义为数据分布问题：让 rejected 直接来自待训练模型，chosen 只做最小事实修正，尽量保持句法和内容长度相近。

这一设计比“原图配正确描述、随机错描述”更接近真实自由生成，但引入 GPT-4V 纠错器和多阶段训练。纠错器若遗漏图像事实或大幅重写，偏好仍可能混入风格信号；因此最小编辑程度和人工质量抽查应属于复现协议。

## 3. 方法详解

第一阶段对每张图从原策略采样响应，自动识别 hallucination 并交给 GPT-4V 生成尽量少改动的正确版本。第二阶段用 ground-truth instruction 与纠正响应对 LoRA 做 SFT，使 policy 与偏好数据更对齐。第三阶段重新采样或使用已对齐分布做 DPO。

标准 DPO 可能同时降低 chosen/rejected 的绝对概率，只保留相对差。OPA-DPO 增加 anchor，要求 chosen 相对参考策略不被压低；image-focus 则强化视觉条件在偏好比较中的作用。部署阶段模型已内化，无额外解码分支。

## 4. 实验设计

### 4.1 设置

以 LLaVA-v1.5 7B/13B 为主，偏好规模约 4.8k 等多个设置。生成基准包括 AMBER、Object HalBench 和 MMHal-Bench，封闭式对象存在性用 POPE。主表同时登记覆盖率、认知错误、CHAIR 与重复率，能检查训练是否靠缩短或模式崩溃取巧。

### 4.2 主结果

| LLaVA-1.5-7B 指标 | Base | OPA-DPO 4.8k | 解读 | 来源 |
|---|---:|---:|---|---|
| AMBER CHAIR ↓ | 7.7 | 2.2 | 明显降低对象虚构 | Table 2 |
| AMBER Cover ↑ | 51.6 | 47.9 | 覆盖下降，存在保守化代价 | Table 2 |
| AMBER HallRate ↓ / Cog ↓ | 34.7 / 4.2 | 11.6 / 0.9 | 生成错误显著下降 | Table 2 |
| MMHal score ↑ / HallRate ↓ | 2.01 / 0.61 | 2.83 / 0.45 | 质量与幻觉共同改善 | Table 2 |
| Object HalBench CHAIR$_S$/$_I$ ↓ | 55.67 / 15.96 | 13.00 / 4.25 | 大幅改善自由生成 | Table 2 |
| POPE adversarial Acc / Precision ↑ | 84.93 / 89.10 | 82.60 / 95.61 | precision 升但 accuracy 降 | Table 2 |

主结果很强，但 Cover 和 POPE accuracy 的下降揭示了 precision–recall 权衡。不能只引用 CHAIR；对面向完整描述的应用，应把是否漏掉真实对象作为同等重要终点。

### 4.3 消融与分析实验

on-policy 是最关键变量：7B 4.8k 设置中，使用 OPA 的 AMBER HallRate 为 11.6，不使用为 22.6；Object HalBench CHAIR$_S$ 为 13 对 23。13B 也呈同方向（HallRate 12.8 对 27.5，CHAIR$_S$ 16.33 对 32.67）。Table 4 进一步显示去掉 image-focus 后重复率升到 15.7%，完整方法为 0.6%，同时 hallucination 指标恶化；anchor 和加权目标也各自有贡献。这支持“策略匹配 + 视觉聚焦”而非普通 DPO 即可解释全部收益，但仍缺少等质量人工纠错器对照与多 seed CI。

## 5. 亮点与贡献

- 把偏好优化的 population mismatch 变成可检验变量。
- 最小纠错让正负响应尽量只在视觉事实处不同。
- 消融同时暴露重复崩溃与覆盖率代价，诊断价值高。

## 6. 局限

强视觉模型参与标注，成本和闭源版本依赖明显。两阶段 LoRA 改变了 reference/policy 关系，公平复现需冻结每一 checkpoint。极大的 CHAIR 改善伴随 Cover、POPE accuracy 下降，可能有更保守的答复边界。纠错只覆盖被检测出的错误，漏检会把噪声写入 chosen。

## 7. 与我的研究关系

OPA-DPO 为“从目标模型自身错误采样是否优于外部模板负例”提供直接 baseline。可将 on-policy 文本纠错与对象删除图结合，并设置 matched sham，判断训练收益来自视觉反事实还是仅来自模型熟悉的语言错误分布。

## 8. 可执行的后续实验

1. 固定偏好规模，比较 on-policy、其他模型错误、随机替换三种 negative。
2. 对 chosen/rejected 计算编辑距离和人类事实准确率，审计最小纠错。
3. 绘制 CHAIR–Cover–length Pareto，而非只报告单一 checkpoint。
4. 在自然缺失图和多编辑器删除图上测试训练迁移。

## 9. 复现清单

- [x] 官方 Figure 3、主结果、on-policy 与 image-focus 消融已登记
- [ ] 固定采样温度、纠错 prompt、GPT-4V 版本
- [ ] 保存每阶段 LoRA checkpoint 与 reference policy
- [ ] 报告偏好对编辑距离、拒答和重复率
- [ ] 联合报告 accuracy/precision/recall、Cover 与长度

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 强调 on-policy 数据而非新 loss |
| 证据强度 | 4/5 | 多基准且 on-policy 消融明确 |
| 可复现性 | 3/5 | 有代码但依赖闭源纠错器 |
| 相关性 | 5/5 | 直接涉及反事实偏好与分布匹配 |

## 11. 来源边界

本文依据 CVPR 2025 官方论文、arXiv 版本与作者代码整理。数字来自 Tables 2–4；对对象删除、matched sham 和 population mismatch 的扩展属于本站分析。
