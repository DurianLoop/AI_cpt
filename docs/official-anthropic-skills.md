# Official Anthropic Skills

本仓库已从官方仓库同步一组适合你的 Anthropic skills。用户后来要求精简，因此只保留文档处理、skill 创建和网页测试相关的官方 skills。

官方仓库：<https://github.com/anthropics/skills>

## 已同步到本仓库

- `skill-creator`：创建和维护自己的 skill。
- `docx`：创建、编辑、分析 Word 文档。
- `pdf`：提取、分析和处理 PDF。
- `pptx`：创建、编辑、分析 PowerPoint 演示文稿。
- `xlsx`：创建、编辑、分析 Excel 表格。
- `webapp-testing`：测试本地网页应用。

## 已按用户要求删除

- `brand-guidelines`
- `claude-api`
- `frontend-design`
- `mcp-builder`
- `theme-factory`

## 为什么适合你

- 你正在搭建可迁移的 AI 工作流仓库，`skill-creator` 很关键。
- 你有资料整理、知识库、repo 对比、提示词沉淀需求，`docx`、`pdf`、`pptx`、`xlsx` 很实用。
- 你已有网页设计和视频演示类 skill，`webapp-testing` 可以补上验证能力。

## 官方 Claude Code 安装方式

在 Claude Code 中，官方 README 推荐先添加 marketplace：

```text
/plugin marketplace add anthropics/skills
```

然后安装需要的插件包：

```text
/plugin install document-skills@anthropics/skills
/plugin install example-skills@anthropics/skills
```

## 本仓库同步方式

如果以后要重新同步官方仓库，可以执行：

```powershell
git -c http.proxy=http://127.0.0.1:7897 -c https.proxy=http://127.0.0.1:7897 clone https://github.com/anthropics/skills.git work\anthropics-skills

Copy-Item -Recurse -Force work\anthropics-skills\skills\docx skills\docx
Copy-Item -Recurse -Force work\anthropics-skills\skills\pdf skills\pdf
Copy-Item -Recurse -Force work\anthropics-skills\skills\pptx skills\pptx
Copy-Item -Recurse -Force work\anthropics-skills\skills\xlsx skills\xlsx
Copy-Item -Recurse -Force work\anthropics-skills\skills\skill-creator skills\skill-creator
Copy-Item -Recurse -Force work\anthropics-skills\skills\webapp-testing skills\webapp-testing
```

## 同步原则

- 保持每个官方 skill 的原始文件夹结构。
- 不改 `SKILL.md` 的 `name` 和 `description`，除非明确 fork 成自己的版本。
- 只同步实际会用的官方 skill，避免把整个示例仓库变成噪音。
