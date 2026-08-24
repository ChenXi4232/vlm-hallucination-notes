---
title: "Locate-then-Sparsify: Attribution Guided Sparse Strategy for Visual Hallucination Mitigation"
description: 以 token/句级幻觉数据归因各层贡献，并将已有 feature steering 转成逐层稀疏强度
authors: [Tiantian Dang, Chao Bi, Shufan Shen, Jinzhe Liu, Qingming Huang, Shuhui Wang]
venue: CVPR
year: 2026
resource_type: 方法论文
direction: Representation / Activation
hallucination_type: [Object hallucination, Sentence-level hallucination]
method_level: [Layer-level, Feature steering]
training: Offline attribution
status: 已精读
source_status: CVPR 2026 接收信息与 arXiv v2 官方论文已核对
review_state: automated
added_at: 2026-08-24
last_verified: 2026-08-24
paper_url: https://arxiv.org/abs/2603.16284
overview_figure: ../assets/images/papers/locate-then-sparsify-overview.png
overview_figure_source: Figure 3 from the official arXiv v2 paper
tags: [Locate-then-Sparsify, LTS-FS, Attribution, Layer-wise steering, CVPR]
---

# Locate-then-Sparsify

<div class="paper-meta"><span>CVPR 2026</span><span>Representation / Activation</span><span>Offline attribution</span><span>已精读</span></div>

[论文原文](https://arxiv.org/abs/2603.16284){ .kb-button .primary }

<div class="paper-tldr"><strong>一句话总结</strong><p>LTS 先用 token 级和句级合成幻觉样本，通过逐层干预估计每层对幻觉的贡献，再把归因分数变成稀疏、层级不同的 steering 强度，可作为 Nullu/VTI 等全层统一注入的外接调度器。</p></div>

## 官方方法概览图

<figure class="paper-figure"><a href="../../assets/images/papers/locate-then-sparsify-overview.png" target="_blank" rel="noopener"><img src="../../assets/images/papers/locate-then-sparsify-overview.png" alt="Locate-then-Sparsify 官方流程"></a><figcaption>官方方法概览图（论文 Figure 3）：双粒度数据、层级归因、稀疏强度与 feature steering 融合。</figcaption></figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 问题 | 现有 feature steering 常对所有层使用同一强度，忽略幻觉贡献的层间异质性 |
| Locate | 用干预比较估计 hallucination/correct/capability 三类指标的逐层贡献 |
| Sparsify | 根据归因选择层并设不同强度，其余层不干预 |
| 兼容性 | 外接 Nullu、VTI，形成 LTS-FS(Nullu/VTI) |
| 评测 | CHAIR、POPE、MME、LLaVA-Bench、延迟与泛化 |

## 2. 研究背景

全局 activation direction 可以降低幻觉，但不同层承担视觉融合、语义组合和输出决策的角色不同。统一注入既可能错过关键层，也可能在无关层破坏通用能力。LTS 将问题改成先归因后稀疏化：只在证据显示与幻觉相关的层使用方向，并以 correct/capability 指标限制副作用。

归因来自合成 hallucination 数据和指定 intervention，未必等于自然生成的真实因果贡献。若归因与最终评价共用数据，层强度还可能过拟合 benchmark；独立 split 和跨模型泛化是必要控制。

## 3. 方法详解

作者构造 token-level 与 sentence-level hallucination 样本，分别捕获局部实体错误和整句不忠实。对各层执行干预，测量 hallucination indicator、correctness indicator 与 preservation indicator 的变化，合成为层归因分数。随后按稀疏率 $r_s$ 保留关键层，并把分数映射为层级 steering intensity。

框架本身不重新发明方向，可接入 Nullu 或 VTI。它主要改变“在哪里、用多强”而非“沿哪个方向”。这有利于做模块化比较，也意味着最终收益同时依赖基础方向质量和归因策略。

## 4. 实验设计

### 4.1 设置

主干包括 LLaVA-v1.5 7B/13B 与 Qwen2.5-VL-7B，baseline 为 Regular、VCD、AGLA、Nullu、VTI。CHAIR 同时报 Recall 和 Length，POPE 覆盖 random/popular/adversarial，另用 MME 和 LLaVA-Bench 检查能力。默认 $r_s=0.5$。

### 4.2 主结果

| 模型 / 指标 | Base steering | LTS-FS | 解读 | 来源 |
|---|---:|---:|---|---|
| LLaVA-7B Nullu CHAIR$_S$/$_I$ ↓ | 50.2 / 13.7 | 46.8 / 13.5 | 稀疏调度改善 Nullu | Table 1 |
| LLaVA-7B VTI CHAIR$_S$/$_I$ ↓ | 47.4 / 13.9 | 35.8 / 11.9 | 对 VTI 提升更大 | Table 1 |
| LLaVA-7B LTS-VTI Recall / Len | VTI 76.2 / 88.9 | 75.4 / 82.2 | 仍有覆盖与长度代价 | Table 1 |
| LLaVA-13B VTI CHAIR$_S$/$_I$ ↓ | 36.3 / 9.2 | 32.0 / 8.8 | 跨规模改善 | Table 1 |
| Qwen LTS-Nullu CHAIR$_S$/$_I$ ↓ | Nullu 27.4 / 7.7 | 23.8 / 6.0 | 跨架构改善 | Table 1 |
| LLaVA-7B POPE Adv Acc/F1 ↑ | Regular 70.13/75.85 | LTS-VTI 73.04/77.32 | 困难负例提升 | Tables 2–3 |

CHAIR 的改善与基础方向相关，LTS-VTI 在 7B 上最明显；但长度 88.9→82.2、Recall 小降，提示部分收益仍可能来自生成收缩。LTS-Nullu 的长度和 Recall 更接近原方法，适合做联合 Pareto 比较。

### 4.3 消融与分析实验

仅 token-level、仅 sentence-level、双粒度相对 Nullu 的 CHAIR$_S$ 为 50.0、47.3、46.8，双粒度 POPE Acc/F1 79.92/82.02 最好，说明局部与全局信号互补。$r_s$ 扫描中 0.5 给出 CHAIR$_S$ 46.8、Recall 76.6、Length 93.2；soft gating 46.7/76.1/94.5，差异很小，说明硬稀疏并非唯一有效形式。论文还报告时间接近基础 steering，并有跨方法/模型泛化；但 layer attribution 数据、强度映射和最终 benchmark 的独立性仍需严格审计。

## 5. 亮点与贡献

- 将方向与层级调度解耦，可直接增强已有 steering。
- 双粒度幻觉归因覆盖 token 和 sentence 两种错误。
- 同时报 Recall、Length、POPE、MME 和时间，评估较完整。

## 6. 局限

离线数据与归因计算不应被省略为“零成本”。合成错误可能决定选层结果。只调整 layer intensity，无法解决基础方向本身纠缠。部分配置仍缩短输出。硬稀疏与 soft gating 接近，机制叙事未必唯一。跨未见 domain 的层排名稳定性尚不充分。

## 7. 与我的研究关系

LTS 是低秩/单 pass 局部 intervention 的直接 baseline。可把层归因换成独立的对象删除 causal effect，再测试是否比合成标签更能迁移；也应区分“可解码层”“可干预层”和“自由生成有效层”。

## 8. 可执行的后续实验

1. 用独立 split 完成归因、稀疏率选择和最终测试。
2. 对象删除、matched sham 与随机 corruption 分别估计层排名，比较 rank stability。
3. 在等 CHAIR 与等长度点比较 uniform、hard sparse、soft gating。
4. 做 layer-matched 随机强度置换，确认收益来自归因顺序。

## 9. 复现清单

- [x] 官方 Figure 3、主表、双粒度与稀疏率消融已登记
- [ ] 固定合成数据生成器、三项指标和归因 split
- [ ] 保存逐层分数、强度、方向 norm
- [ ] 报告实际延迟、触发层数与显存
- [ ] 加入长度/Recall 匹配比较和 bootstrap CI

## 10. 综合评分

| 维度 | 评分 | 理由 |
|---|---:|---|
| 新颖性 | 4/5 | 归因指导层级稀疏 steering |
| 机制证据 | 3/5 | 双粒度消融好，选择独立性待加强 |
| 效率 | 4/5 | 部署接近基础 steering |
| 相关性 | 5/5 | 直接支持局部低成本干预 |

## 11. 来源边界

本文依据 arXiv:2603.16284 v2 与 CVPR 2026 接收信息整理。数字来自 Tables 1–5；对 split 独立性、对象删除归因和等长度比较属于本站分析。
