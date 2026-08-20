---
title: "Hallucination Begins Where Saliency Drops"
description: 用 attention×gradient 衡量输出 token 对历史输出的显著性，并以 SGRS 拒绝低显著候选、以 LocoRE 强化局部文本依赖
authors: [Xiaofeng Zhang, Yuanchao Zhu, Chaochen Gu, Xiaosong Yuan, Qiyan Zhao, Jiawei Cao, Feilong Tang, Sinan Fan, Yaomin Shen, Chen Shen, Hao Tang]
venue: arXiv
year: 2026
resource_type: 方法论文
direction: Attention Head / Path
secondary_directions: [Token / Logit, Long-form / Semantic Drift]
hallucination_type: [Object hallucination, Context-drift hallucination]
method_level: [Attention saliency, Candidate rejection, Attention reweighting]
training: Training-free
status: 已精读
source_status: arXiv v1、官方 LaTeX 素材、表格与代码链接已核对
review_state: automated
arxiv_version: v1
last_verified: 2026-08-20
paper_url: https://arxiv.org/abs/2601.20279
code_url: https://github.com/zhangbaijin/LVLMs-Saliency
overview_figure: ../assets/images/papers/saliency-overview.png
overview_figure_source: LocoRE structure figure in the official arXiv v1 LaTeX source package
tags: [Saliency, Attention gradient, SGRS, LocoRE, Rejection sampling, CHAIR, POPE]
---

# Hallucination Begins Where Saliency Drops

<div class="paper-meta"><span>arXiv 2026</span><span>Attention × Gradient</span><span>SGRS</span><span>LocoRE</span></div>

[arXiv](https://arxiv.org/abs/2601.20279){ .kb-button .primary } [Code](https://github.com/zhangbaijin/LVLMs-Saliency){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>论文发现幻觉 token 的关键异常不是单纯少看图，而是对最近输出 token 的 attention×gradient saliency 下降；SGRS 在提交候选前拒绝低显著 token，LocoRE 则在下一步放大对局部输出历史的 attention，组成“筛选当前、巩固下一步”的闭环。</p></div>

## 官方方法概览图

<figure class="paper-figure">
  <a href="../../assets/images/papers/saliency-overview.png" target="_blank" rel="noopener">
    <img src="../../assets/images/papers/saliency-overview.png" alt="Local Coherence Reinforcement 对局部输出窗口的注意力增强结构">
  </a>
  <figcaption>官方 LocoRE 结构图，来自 arXiv v1 source 的 <code>method.png</code>。原文未提供一张同时覆盖 SGRS 与 LocoRE 的 pipeline；SGRS 的候选拒绝流程以论文 Algorithm 1 为准。</figcaption>
</figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 分析工具 | LVLMs-Saliency：\(|A\odot \nabla_A L|\) 的 causal lower-triangular saliency |
| 核心发现 | hallucinated token 对先前输出 token 的 saliency 显著降低 |
| SGRS | top-K 候选逐个计算 saliency，以历史窗口自适应阈值接受/拒绝 |
| LocoRE | 放大下一 token 对最近 \(w_s\) 个输出位置的 attention |
| 模型 | LLaVA-1.5 7B/13B、Qwen2-VL-7B、InternVL 7B/13B |
| 评测 | POPE、CHAIR、MME、LLaVA-Wild、MM-Vet、VizWiz、ScienceQA |
| 适合角色 | gradient-aware diagnostic；context-memory intervention baseline |

## 2. 研究背景与核心矛盾

许多 hallucination 分析只读 forward attention，把“权重高”近似成“因果影响大”。但某个 attention edge 即便数值高，也可能对目标 logit 不敏感；反之，小权重可能具有大梯度。论文因此将 attention 与其梯度相乘，并把重点从 image-to-output 转向 output-to-output：生成历史如果不再影响下一 token，模型更容易靠局部语言先验续写出不一致对象。

这里必须区分 **视觉 grounding** 与 **文本一致性**。低 output-to-output saliency 说明模型忘记自己刚说过什么，不直接证明它忽略图像。LocoRE 强化文本历史也可能让一个已经错误的对象持续得更一致。论文用 SGRS 先过滤再强化来缓解这个风险，但“saliency 低导致 hallucination”的因果措辞仍强于现有观察与干预证据。

| 主张 | 支持证据 | 边界 |
|---|---|---|
| attention×gradient 比纯 attention 更能区分真假 token | LLaVA 与 Qwen2-VL 的分布分析 | 需要独立标签、layer/head 稳定性与 AUROC |
| 最近输出记忆下降是 onset 信号 | 正确/幻觉 token 的时序显著性差异 | 可能是错误发生后的伴随现象 |
| SGRS 可阻止错误进入上下文 | SGRS+LocoRE 优于 LocoRE | 每个候选梯度计算代价高 |
| LocoRE 能修复长期一致性 | CHAIR/POPE/MME 与通用 benchmark | 只强化文本，不保证视觉真实性 |

## 3. 方法详解

### 3.1 LVLMs-Saliency

对第 \(l\) 层、第 \(h\) 个 head 的 attention matrix \(A^{(l,h)}\)，针对候选目标的 loss 求梯度并构造：

\[
S^{(l,h)}=\operatorname{tril}\left(\left|A^{(l,h)}\odot \nabla A^{(l,h)}\right|\right).
\]

随后在 head 上求和并做层内 \(\ell_2\) normalization。triangular mask 保留自回归因果结构；绝对值保留影响幅度而丢掉促进/抑制方向。因此该量适合描述“敏感度”，不宜直接解释为正向支持。

### 3.2 SGRS：Saliency-Guided Rejection Sampling

生成位置 \(P\) 先从 top-K 池采样候选 \(c_i\)，对目标层与历史输出位置 \(\mathcal J\) 汇总 saliency：

\[
\mathcal S(c_i)=\frac{1}{|\mathcal L||\mathcal J|}\sum_{l\in\mathcal L}\sum_{j\in\mathcal J}\bar S^{(l)}_{P,j}.
\]

阈值不是全局常数，而是最近 \(W\) 个已接受 token 的平均 saliency 乘 \(\alpha\)。候选低于阈值就重采，最多尝试 \(R\) 次；全部失败时退回 saliency 最高者。这将 diagnostic 变成 decoding policy，但候选逐次 backward 很可能是全方法的主要延迟来源。

### 3.3 LocoRE：Local Coherence Reinforcement

预测位置 \(P+1\) 时，对距离当前不超过 \(w_s\) 的历史输出位置，将 attention 乘以 \(1+\beta\)。原文写为对 attention weights 修改后再进入 softmax/weighted sum；实现时要确认 hook 作用在 pre-softmax score 还是 post-softmax probability，因为两者不等价，后者还需重新归一化。

SGRS 负责当前 token 的入口检查，LocoRE 负责下一步继续记住最近输出。闭环直觉合理，但两个组件都以 output context 为中心，视觉 token 仅通过模型原始计算间接参与。

## 4. 实验设计与关键结果

论文在 LLaVA-1.5、Qwen2-VL 与 InternVL 的多个尺寸上验证，并覆盖 hallucination 与通用能力。LLaVA-1.5-7B 主表中：

| 方法 | POPE F1 / Acc ↑ | CHAIR C_S / C_I ↓ | Recall ↑ | MME Total ↑ |
|---|---:|---:|---:|---:|
| Beam Search | 85.4 / 84.0 | 51.0 / 15.2 | 75.2 | 565.34 |
| LocoRE | 86.9 / 87.3 | 38.4 / 11.2 | 75.4 | 656.66 |
| SGRS + LocoRE | **87.0 / 87.5** | **35.6 / 8.2** | 75.4 | **668.33** |

组合相对 LocoRE 继续降低 C_I，支持候选过滤具有增量作用；Recall 基本不变，至少在表中没有明显“少说对象”的退化。与不同论文的 referenced numbers 比较仍应谨慎：prompt、长度、采样、模型 patch 和数据版本可能不同。

通用 benchmark 的价值是检查 attention 强化是否破坏问答与推理，不过这些测试无法完全排除 output repetition、过度保守或错误自洽。最关键的补充应是逐 token detection AUROC/lead time、平均候选 backward 次数、tokens/s 与显存峰值。

## 5. 亮点与贡献

- 用 gradient 修正“只看 attention weight”的解释漏洞，提供更接近局部敏感度的诊断量。
- 把 hallucination onset 定位到 output-token memory，而非笼统地说“视觉注意力不足”。
- 自适应历史阈值避免一个跨句长、跨样本固定 saliency cutoff。
- SGRS 与 LocoRE 分别负责防止错误写入和防止近期上下文被遗忘，组件分工清晰。
- 多模型、多尺寸与通用 benchmark 让架构迁移性比单一 LLaVA 实验更可信。

## 6. 局限、指标漏洞与审稿风险

1. **梯度成本高。** top-K 候选逐一或多次 backward 与“inference-time lightweight”存在张力，必须报告端到端延迟。
2. **显著性不是因果贡献。** \(|A\odot\nabla A|\) 是一阶局部敏感度，受 scale、saturation 与 gradient noise 影响。
3. **丢失符号。** 绝对值混合正负作用，高 saliency 可能是强抑制而非强支持。
4. **文本自洽不等于视觉真实。** 强化近期输出可能巩固早期错误，组合收益不能自动证明视觉 grounding 增强。
5. **实现语义需澄清。** attention multiplication 发生在 softmax 前后会改变数学与缓存实现。
6. **阈值冷启动。** 输出历史很短或 saliency 分布跨层/模型变化时，历史均值可能不稳定。

## 7. 与我的研究关系

该论文提供了一个很好的三方对照：纯 attention、attention×gradient、真实 causal ablation。可在同一 token 上与 VR、PD、RBC 和 Role-Break score 比较 detection lead time。如果 saliency drop 早于视觉依赖下降，它更像上下文记忆故障；若两者同步，才支持跨模态 grounding 崩溃。

**Baseline 适合度：Medium。** 诊断价值高，但完整 SGRS 的 backward 成本可能不适合大规模生成；LocoRE 单独实现较轻。

## 8. 可执行的后续实验

| 实验 | Research question | 对照 | 输出 | 预期/失败解释 | 成本 |
|---|---|---|---|---|---|
| E1 Metric ladder | saliency 是否优于 attention？ | A、A×grad、zero-ablation | AUROC、lead time | 若 ablation 最稳，gradient 仅 proxy | Medium |
| E2 Error-lock test | LocoRE 会不会巩固早期错误？ | 注入错误 prefix | error persistence、recovery | persistence 上升即反例 | Low |
| E3 Visual coupling | output saliency 与视觉依赖是否同步？ | VR/PD/RBC | cross-correlation | 分离则机制不同 | Medium |
| E4 Cost audit | SGRS 的真实代价？ | greedy、beam、VCD | tokens/s、backward 次数、VRAM | 候选重试主导延迟 | Low |
| E5 Signed saliency | 符号信息有用吗？ | absolute vs signed/positive-only | detection 与 CHAIR | signed 更可解释 | Medium |

## 9. 复现清单

- [x] arXiv v1、官方 LocoRE 图、算法、主表与代码链接已核对
- [ ] 固定目标层、head 聚合、loss 定义和 normalization 维度
- [ ] 明确 LocoRE 在 pre-/post-softmax 的插入点与再归一化
- [ ] 记录 K、R、W、α、β、\(w_s\) 与候选缓存策略
- [ ] 报告 token-level detection AUROC、lead time 与错误类型分层
- [ ] 报告 wall-clock latency、显存、平均重试次数和生成长度

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 新颖性 | 4.0 | 将 gradient-aware saliency 与闭环解码结合 |
| 机制证据 | 3.5 | 有分析与干预，但 saliency 的因果表述仍偏强 |
| 实验完整性 | 4.0 | 多架构、hallucination 与通用 benchmark |
| 可复现性 | 3.5 | 有代码，梯度与 attention hook 细节敏感 |
| 与当前研究相关性 | 4.5 | 直接连接 token onset、head/path 与干预 |

## 11. 检索标签与来源边界

`requires training: no` · `requires gradients at inference: SGRS yes` · `external model: no` · `attention intervention: yes` · `visual-token-specific: no` · `baseline suitability: medium`

本页依据 [arXiv:2601.20279 v1](https://arxiv.org/abs/2601.20279) PDF、官方 LaTeX source 与作者给出的 [LVLMs-Saliency 代码仓库](https://github.com/zhangbaijin/LVLMs-Saliency)，核对日期为 2026-08-20。官方素材只有 LocoRE 的结构图，没有覆盖 SGRS+LocoRE 的单张 pipeline，因此本站没有把自绘图伪装成官方 overview；SGRS 以原文算法和公式整理。
