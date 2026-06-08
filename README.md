# AI Prompts and Skills

这是我的个人 AI 工作流仓库，用来迁移和管理全局提示词、常用任务模板和 skills。

## 怎么在对话里提醒使用 Skill

对话时可以直接点名 skill，例如：

```text
用 humanizer 帮我把这段文字去 AI 味。
用 arxiv 帮我找几篇相关论文。
用 plan 先给我写一个执行计划，不要直接开工。
用 popular-web-designs 参考成熟网站风格做页面。
用 kb-retriever 从我的知识库里检索答案。
```

如果不确定该用哪个，可以这样问：

```text
这件事适合用哪个 skill？先帮我判断，再执行。
```

## 全局提示词

- `prompts/global.md`：通用协作提示词，包含“人类-AI 协作版乔哈里视窗模型”。
- `prompts/github-repo-search.md`：从 GitHub 搜索和筛选 repo 的提示词模板。

## Skills 清单

### 写作与表达

- `humanizer`：把文本去 AI 味，改得更自然、更像真人表达。
- `research-paper-writing`：辅助写 ML/AI 论文，包括结构、实验、引用和投稿准备。
- `docx`：创建、编辑和分析 Word 文档。

### 研究与资料

- `arxiv`：按关键词、作者、分类或论文 ID 搜索 arXiv。
- `kb-retriever`：从本地知识库目录检索信息，适合 PDF、Excel 和大段资料。
- `pdf`：处理 PDF，包括读取、表单和结构化信息。

### 分析与表格

- `jupyter-live-kernel`：通过 live Jupyter kernel 做迭代 Python 分析。
- `xlsx`：创建、编辑和分析 Excel 表格。

### 规划与创意

- `plan`：只写计划，不直接执行；适合复杂任务开工前拆解。
- `ideation`：基于约束生成项目创意，适合“我想做点什么但没方向”。
- `skill-creator`：创建、维护和改造自己的 skill。

### 设计与网页

- `claude-design`：生成一次性 HTML 设计产物，例如 landing、deck、prototype。
- `sketch`：快速做 2-3 个 HTML 草图方案，用来比较方向。
- `popular-web-designs`：参考成熟网站和设计系统生成 HTML/CSS。
- `web-design-engineer`：构建高质量网页、前端界面、原型和可视化。
- `webapp-testing`：测试本地网页应用，验证交互和页面行为。

### 图像与演示

- `gpt-image-2`：GPT Image 2 图像生成/编辑提示词与工作流。
- `powerpoint`：创建、读取和编辑 `.pptx` 演示文稿。
- `pptx`：Anthropic 官方 PowerPoint 处理 skill。
- `web-video-presentation`：把文章或口播稿做成点击驱动的网页式视频演示。

## 目录结构

```text
.
├─ prompts/
├─ skills/
├─ docs/
├─ setup-notes.md
└─ README.md
```

## 迁移原则

- 提示词和 skill 尽量使用相对路径。
- 不把 API Key、账号密码、私人信息或公司机密写进仓库。
- 中文 Markdown 统一使用 UTF-8 编码。
- 如果包含敏感内容，优先使用私有仓库。
