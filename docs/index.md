---
title: VLM Hallucination Research Atlas
description: 机制导向、证据约束、面向可复现实验的 VLM 幻觉研究知识库
hide:
  - toc
---

<div class="kb-hero" markdown>
<span class="kb-eyebrow">MECHANISM-FIRST RESEARCH KNOWLEDGE BASE</span>

# 追踪幻觉，直到<em>视觉证据</em>断裂的位置

围绕 VLM/LVLM hallucination 的解释、检测与缓解，组织 token、attention head、representation 与 logit 层面的论文证据，并将每篇论文转化为可比较、可复现的研究资产。

<div class="kb-actions">
  <a class="kb-button primary" href="papers/">浏览论文库 →</a>
  <a class="kb-button" href="research-map/">查看研究版图</a>
  <a class="kb-button" href="guides/paper-card/">新建 Deep Paper Note</a>
</div>
</div>

<div class="stat-grid">
  <div class="stat-card"><strong>7</strong><span>Deep Paper Notes</span></div>
  <div class="stat-card"><strong>5</strong><span>核心研究方向</span></div>
  <div class="stat-card"><strong>4</strong><span>干预层级</span></div>
  <div class="stat-card"><strong>9</strong><span>待整理来源</span></div>
</div>

## 研究入口

<div class="atlas-grid">
  <a class="atlas-card" href="directions/token-logit/">
    <span class="index">01 · TOKEN</span>
    <h3>Token / Logit 反事实</h3>
    <p>真实图像、空白图像与反事实图像下的候选分布差异。</p>
  </a>
  <a class="atlas-card" href="directions/attention-heads/">
    <span class="index">02 · HEAD</span>
    <h3>Attention Head / Path</h3>
    <p>定位视觉敏感头、语言先验路径与生成阶段中的异常作用。</p>
  </a>
  <a class="atlas-card" href="directions/representation/">
    <span class="index">03 · STATE</span>
    <h3>Representation / Activation</h3>
    <p>残差流、MLP、KV 与低秩编辑中的幻觉表征和可控方向。</p>
  </a>
  <a class="atlas-card" href="directions/evaluation/">
    <span class="index">04 · AUDIT</span>
    <h3>Evaluation / Trade-off</h3>
    <p>同时审计 CHAIR、POPE、recall、覆盖率与生成退化。</p>
  </a>
</div>

## 当前研究主线

```mermaid
flowchart LR
    A[反事实图像输入] --> B[Token / Head / Logit 诊断]
    B --> C{幻觉风险}
    C -->|低风险| D[原始解码]
    C -->|高风险| E[候选重排或局部干预]
    D --> F[质量与 Recall 审计]
    E --> F
```

!!! note "阅读原则"
    视觉依赖不等于事实正确，attention weight 也不等于因果贡献。本知识库要求每篇论文同时记录：核心假设、可执行实现、benchmark/metric、baseline 价值、反事实启发与审稿风险。

## 最近接入

- [Intervene-All-Paths](papers/intervene-all-paths.md)：跨对齐格式的多路径 head intervention。
- [Vision-aware Head Divergence](papers/vision-aware-head-divergence.md)：用有图/无图 head output divergence 定位视觉敏感头。
- [Self-Introspective Decoding](papers/self-introspective-decoding.md)：利用低重要度视觉 token 构造上下文相关对比分支。
- [M3ID](papers/m3id.md)：放大有图与无图分布差异，抵抗 language prior dominance。

<p class="source-warning">知识卡包含个人研究解读。标记为“待核对”的条目不可作为最终论文写作中的事实依据，引用前应回查论文原文与公开代码。</p>
