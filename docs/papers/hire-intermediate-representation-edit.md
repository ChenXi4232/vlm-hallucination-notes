---
title: "Hallucination-aware Intermediate Representation Edit in Large Vision-Language Models"
description: HIRE 用可训练的 Editor 分离语义与幻觉表征，再由 Router 只在高风险 token 上执行可调强度的中间表示编辑
authors: [Wei Suo, Hanzu Zhang, Lijun Zhang, Ji Ma, Peng Wang, Yanning Zhang]
venue: arXiv
year: 2026
resource_type: 方法论文
direction: Representation / Activation
secondary_directions: [Token / Logit, Detection / Routing]
hallucination_type: [Object hallucination, Attribute hallucination, Relation hallucination]
method_level: [Attention output, Intermediate representation, Token-level router]
training: Lightweight module training
status: 已精读
source_status: arXiv v1、官方 LaTeX 素材、表格与代码链接已核对
review_state: automated
arxiv_version: v1
last_verified: 2026-08-20
paper_url: https://arxiv.org/abs/2603.29405
code_url: https://github.com/ASGO-MM/HIRE
overview_figure: ../assets/images/papers/hire-overview.png
overview_figure_source: Overview figure in the official arXiv v1 LaTeX source package
tags: [HIRE, Representation editing, Router, Autoencoder, DPO, CHAIR, POPE, AMBER]
---

# HIRE：Hallucination-aware Intermediate Representation Edit

<div class="paper-meta"><span>arXiv 2026</span><span>Representation Editing</span><span>Router</span><span>Lightweight Training</span></div>

[arXiv](https://arxiv.org/abs/2603.29405){ .kb-button .primary } [Code](https://github.com/ASGO-MM/HIRE){ .kb-button }

<div class="paper-tldr"><strong>一句话总结</strong><p>HIRE 不改动 LVLM 主干参数：Editor 用真实/诱导幻觉表征学习保持语义、移动幻觉分量的 token-specific edit direction，Router 再根据首层表示决定当前 token 是否需要编辑，并用强度 α 控制抑制或放大幻觉。</p></div>

## 官方方法概览图

<figure class="paper-figure">
  <a href="../../assets/images/papers/hire-overview.png" target="_blank" rel="noopener">
    <img src="../../assets/images/papers/hire-overview.png" alt="HIRE 的 Editor 与 Router 训练和推理框架">
  </a>
  <figcaption>官方 HIRE 总览图，来自 arXiv v1 LaTeX source 中的 <code>4k_training.pdf</code>：Editor 通过语义不变性与幻觉差异学习编辑方向，Router 通过偏好优化学习何时触发编辑。</figcaption>
</figure>

## 1. 论文速览

| 维度 | 内容 |
|---|---|
| 核心问题 | 如何避免重训 LVLM 与双分支 contrastive decoding，同时只修改高风险 token |
| 关键模块 | 双编码器 Editor、二分类 Router、Hallucination Regulator |
| 编辑位置 | Transformer attention-layer representation；Router 一次决策控制后续层 |
| 训练资料 | MSCOCO：Editor 2,000 样本，Router 8,000 样本 |
| 模型 | LLaVA-1.5、InstructBLIP |
| 评测 | CHAIR、POPE、AMBER，另含效率、层位、数据量与稳定性分析 |
| 适合角色 | learned representation-edit baseline；token risk routing baseline |

## 2. 研究背景与核心矛盾

训练式方法的代价在于更新大模型，contrastive decoding 的代价则是几乎每一步都运行两条生成分支。HIRE 试图把代价转移到小模块：主干冻结，离线学习“如何编辑”和“何时编辑”，在线仅对 Router 判为高风险的 token 注入方向。它并不是 training-free；准确说法是 **frozen-backbone、lightweight-module training**。

论文建立在两个假设上。第一，真实与幻觉回答的中间表示存在可利用的差异，但语义与幻觉分量纠缠，不能直接减均值方向。第二，并非所有 token 都需要被修改，功能词或已正确 grounded 的 token 若被统一处理，可能损害连贯性。Editor 对应第一个假设，Router 对应第二个假设。

| 主张 | 论文证据 | 仍需注意 |
|---|---|---|
| 表征编辑可替代双分支解码 | CHAIR/POPE/AMBER 与 TFLOPs 对比 | 训练小模块与数据构造仍有成本 |
| Router 能减少无效编辑 | 组件消融与 TFLOPs | Router 标签来自候选序列偏好，不是独立 token 真值 |
| α 可连续控制幻觉 | α 从负值到正值的 CHAIR 曲线 | 负 α 放大幻觉不等于方向具备因果唯一性 |
| 语义能够在编辑后保留 | semantic encoder 与重建/对比目标 | 主要输出指标仍偏 object hallucination |

## 3. 方法详解

### 3.1 Editor：把语义保持与幻觉移动拆开

对第 \(l\) 层、第 \(t\) 个 token 的 attention-layer representation \(h_{tl}\)，Editor 使用语义编码器 \(E_{sem}\) 与幻觉编码器 \(E_{hal}\)：

\[
h_{tl,sem}=E_{sem}(h_{tl}),\qquad h_{tl,hal}=E_{hal}(h_{tl}).
\]

训练数据包含同一语义下的正、负视觉输入。作者以真实图像产生低幻觉表示，以破坏视觉信息的输入产生高幻觉表示，要求 semantic branch 对两者保持相近，同时让 hallucinatory branch 表达差异。每层的平均差异形成 \(\delta_l\)。语义分量作为 query，幻觉分量加上或减去 \(\delta_l\) 作为 key/value，经 attention fusion 和 decoder 得到两个重建结果，其差定义为 token-specific edit direction \(\Delta_{tl}\)。因此 HIRE 不是把所有 token 减去一个固定向量，而是由当前表示生成方向。

### 3.2 Router：把“是否编辑”变成序列偏好问题

Router 是读取第一层 token representation 的 MLP，输出二元动作 \(c_t\)。若 \(c_t=1\)，Editor 在后续层执行：

\[
h^{aug}_{tl}=h_{tl}+\alpha\Delta_{tl};
\]

否则保留原表示。Router 的训练不是直接使用人工 token hallucination 标签。作者对同一图像生成多条采用不同编辑动作轨迹的候选句，用 CHAIR_I 选出最可信与最差的一对，再用 DPO 学习偏好动作序列。这个设计让监督落在最终句子质量，但也意味着 Router 学到的是 CHAIR 定义下的序列偏好，迁移到属性、关系或非 COCO 类别时需要重新验证。

### 3.3 Hallucination Regulator

\(\alpha>0\) 沿低幻觉方向编辑，\(\alpha<0\) 反向放大，绝对值控制强度。它提供了一个很直观的 dose-response 实验接口；但“可控创意”需要独立的人类偏好与多样性评测，不能只用 CHAIR 上升或下降代替。

## 4. 实验设计与关键结果

Editor 在 MSCOCO 2,000 样本上训练 5 epochs，Router 在 8,000 样本上训练 100 epochs；两者使用 SGD、初始学习率 \(10^{-2}\)，实验使用 4 张 3090。评测覆盖 CHAIR 的 500 张 COCO 图像、POPE 的 9,000 个二值问答，以及同时含生成式和判别式任务的 AMBER。

| 设置 | Baseline | HIRE | 读法 |
|---|---:|---:|---|
| LLaVA-1.5，CHAIR，512 tokens | C_S 51.3 / C_I 16.8 | **30.2 / 9.7** | 长生成改善明显 |
| InstructBLIP，CHAIR，512 tokens | 51.0 / 24.2 | **39.0 / 11.5** | object-level 降幅更大 |
| LLaVA-1.5，POPE all | Acc 82.04 / F1 80.42 | **87.27 / 87.23** | 同时降低 yes/no 偏差风险需看三 split |
| InstructBLIP，POPE all | 79.14 / 79.31 | **85.27 / 85.42** | 相对 Octopus 仍有提升 |

效率表中 LLaVA 长描述 baseline 为 10.23 TFLOPs，HIRE 为 11.81，明显低于表中约 20 TFLOPs 的双分支方法；但短描述与 InstructBLIP 上仍有额外开销。结果支持“低于双分支”，不应写成“零开销”。AMBER 总分相对 baseline 分别提高 7.54 与 6.38。论文还报告 α 曲线、编辑层选择、训练数据量和五个随机种子的稳定性，这些对复现比单个 SOTA 数字更重要。

## 5. 亮点与贡献

- 将“方向估计”和“触发时机”拆为 Editor/Router，结构上比全 token 静态 steering 更清晰。
- 用 token-specific direction 避免把全局均值差直接施加到不同语境。
- 用序列级 CHAIR 偏好训练 Router，绕开昂贵 token-level 人工标注。
- 同时报告长/短描述、判别式与生成式任务以及 TFLOPs，能看到质量—成本折中。
- α 的正负干预提供可检验的剂量响应，而不只是一次性的 on/off ablation。

## 6. 局限、指标漏洞与审稿风险

1. **并非 training-free。** 冻结 LVLM 不等于无训练；Editor/Router 仍依赖 10k 级样本、候选生成与四卡训练。
2. **监督与评测耦合。** Router 用 CHAIR_I 形成偏好，又在 CHAIR 上验证，可能偏向 COCO object vocabulary。
3. **第一层一次路由较粗。** 同一 token 在不同深层的风险可能变化，单一动作控制所有后续层限制了定位精度。
4. **正负图像构造是关键混杂。** 视觉破坏产生的表示差可能包含 OOD 噪声，不全是自然幻觉方向。
5. **“语义保持”证据有限。** 需要更系统的 CIDEr/SPICE、回答相关性、细节覆盖与人工评估。
6. **可控幻觉主张较宽。** 负 α 增加 CHAIR 只能说明能推高错误对象，不证明能生成有用、可控的创造性内容。

## 7. 与我的研究关系

HIRE 是连接 detection 与 intervention 的重要 baseline：Router 对应风险探针，Editor 对应 representation actuator。可把现有 VR、PD、RBC 或 Role-Break 特征作为 Router 输入，测试浅层表征是否足以预测后续幻觉；也可把 Editor 固定，只替换路由信号，拆解收益来自“方向更好”还是“触发更准”。

**Baseline 适合度：High（representation 组），Medium（低算力组）。** 在线效率比 dual decoding 好，但复现需要训练小模块与生成偏好轨迹。

## 8. 可执行的后续实验

| 实验 | 问题 | 对照 | 指标 | 失败解释 | 成本 |
|---|---|---|---|---|---|
| E1 Router swap | Router 是否真正识别风险？ | always-on、random、entropy、VR-router | CHAIR/Recall/触发率 | 收益主要来自 Editor | Medium |
| E2 Layer-local routing | 一次路由是否过粗？ | first-layer vs per-layer | 性能、延迟、路由一致性 | 深层风险不可提前预测 | Medium |
| E3 Label transfer | CHAIR 监督能否迁移？ | COCO→AMBER attribute/relation | AUROC、AMBER 子类 | Router 学到对象词表 | Medium |
| E4 Direction placebo | \(\Delta\) 是否有因果特异性？ | shuffled、orthogonal、sign flip | dose-response | 只是一般 activation 扰动 | Low |
| E5 Quality frontier | α 如何影响保真与细节？ | α sweep | CHAIR、Recall、CIDEr、length | 通过少说话降幻觉 | Low |

## 9. 复现清单

- [x] arXiv v1、官方方法图、公式、主表与代码链接已核对
- [ ] 冻结真实/破坏图像对的生成方式与随机种子
- [ ] 记录 Editor 输入层、latent dimension、loss 权重和注入 hook
- [ ] 复现 Router 候选轨迹、group size=10 与 DPO pair 选择
- [ ] 同时报触发率、TFLOPs、wall-clock latency、CHAIR 与 object recall
- [ ] 对属性/关系子集进行跨类型迁移测试

## 10. 综合评分

| 维度 | 评分（1–5） | 理由 |
|---|---:|---|
| 新颖性 | 4.0 | token-specific Editor 与 Router 联合设计有辨识度 |
| 机制证据 | 3.5 | 有方向强度和组件消融，仍缺更强 placebo/迁移验证 |
| 实验完整性 | 4.0 | 两模型三 benchmark、长短生成和效率均覆盖 |
| 可复现性 | 3.5 | 代码已链接，但训练链路与偏好数据较复杂 |
| 与当前研究相关性 | 4.5 | 直接对应 risk detection + representation intervention |

## 11. 检索标签与来源边界

`requires LVLM finetuning: no` · `requires auxiliary training: yes` · `paired visual perturbation: yes` · `token routing: yes` · `dual inference: no` · `baseline suitability: high`

本页依据 [arXiv:2603.29405 v1](https://arxiv.org/abs/2603.29405) PDF、官方 LaTeX source 与论文给出的 [HIRE 代码仓库](https://github.com/ASGO-MM/HIRE)，核对日期为 2026-08-20。论文 source 使用 ICLR 2026 camera-ready 样式，但当前可核验公开记录是 arXiv，因此 venue 保守记为 arXiv；若后续出现正式 proceedings，应再更新 venue 与结果版本。
