# VLM Hallucination Research Atlas

面向个人研究工作的 VLM/LVLM hallucination 论文知识库。网站采用 **MkDocs Material + GitHub Pages**，论文笔记以 Markdown 和 YAML front matter 保存。

本仓库只保存可公开内容。未成熟想法、实验日志、内部结果和未发表假设存放在私有仓库 `vlm-hallucination-lab`，两边只通过稳定 ID（如 `EXP-HEAD-017`）关联。

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

## 双仓库本地备份（Windows）

已登录 GitHub 后，在 PowerShell 中运行：

```powershell
.\scripts\sync-repositories.ps1
```

脚本默认将公开与私有仓库克隆或快进同步到 `F:\Repositories`。可用 `-Root` 指定其他目录。

## 发布边界

- Public：Deep Paper Notes、Survey、Benchmark/Dataset、Method Taxonomy、整理后的 Reading Notes、Published Research。
- Private：未成熟 idea、实验日志、Codex tasks、内部结果、失败实验和未发表 hypothesis。
- 不要把私密文件放在本仓库的“未导航目录”；公开仓库中的所有已提交文件都可能被读取。
- CI 会运行 `scripts/check_public_boundary.py`，拦截常见私有目录、模型权重、原始日志和大型文件。

## 内容可靠性

论文笔记是研究解释资产，不替代原文。每张卡片都应标记阅读状态与来源核对状态；没有证据的实验结果、venue 或代码链接不得补写。
