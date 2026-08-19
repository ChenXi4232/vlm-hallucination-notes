# VLM Hallucination Research Atlas

面向个人研究工作的 VLM/LVLM hallucination 论文知识库。网站采用 **MkDocs Material + GitHub Pages**，论文笔记以 Markdown 和 YAML front matter 保存。

## 本地使用

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_indexes.py
mkdocs serve
```

## 添加论文

1. 复制 `docs/guides/paper-card.md` 到 `docs/papers/<slug>.md`。
2. 填写 front matter 与正文，资料不足处明确标注“待核对”。
3. 运行 `python scripts/build_indexes.py`。
4. 运行 `mkdocs build --strict`。
5. 提交到 `main` 后，GitHub Actions 自动部署 Pages。

## 分类原则

- **研究方向**：Token/Logit、Attention Head/Path、Representation/Activation、Long-form Drift、Evaluation。
- **资源类型**：方法论文、综述、Benchmark/Metric、Dataset、实验笔记。
- **论文来源**：视觉会议、NLP 会议、ML 会议、arXiv/OpenReview。

一篇论文通过 front matter 同时拥有多个标签，避免只能放进一个文件夹。

## 内容可靠性

论文笔记是研究解释资产，不替代原文。每张卡片都应标记阅读状态与来源核对状态；没有证据的实验结果、venue 或代码链接不得补写。
