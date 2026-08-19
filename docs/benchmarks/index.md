---
title: Benchmarks / Datasets
description: 评测协议、指标漏洞与数据来源的统一入口
---

# Benchmarks / Datasets

评测资源必须与方法论文分开维护，因为同一个 hallucination rate 可能对应不同标注单位、回答格式与 recall 代价。

<div class="atlas-grid">
  <a class="atlas-card" href="../library/benchmarks/"><span class="index">EVAL</span><h3>Benchmark / Metric</h3><p>CHAIR、POPE 等评测协议、指标方向与已知漏洞。</p></a>
  <a class="atlas-card" href="../library/datasets/"><span class="index">DATA</span><h3>Dataset</h3><p>训练、检测、反事实编辑与细粒度标注资源。</p></a>
</div>

## 最低报告要求

- 明确样本单位、claim/token/sentence/image 级别。
- 同时报告 hallucination、recall/coverage、长度、重复与一般能力。
- 区分 zero-shot detector、需要 ground truth 的 evaluator 与 mitigation 方法。
- 给出阈值选择集，避免在测试集上调参。
