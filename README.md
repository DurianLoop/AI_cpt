# AI Prompts and Skills

这是一个用于迁移和管理个人 AI 工作流资产的仓库，包括全局提示词、常用任务模板、skills 和安装记录。

## 目录结构

```text
.
├─ prompts/
│  ├─ global.md
│  └─ github-repo-search.md
├─ skills/
│  ├─ brand-guidelines/
│  ├─ claude-api/
│  ├─ docx/
│  ├─ frontend-design/
│  ├─ gpt-image-2/
│  ├─ kb-retriever/
│  ├─ mcp-builder/
│  ├─ pdf/
│  ├─ pptx/
│  ├─ skill-creator/
│  ├─ theme-factory/
│  ├─ webapp-testing/
│  ├─ web-design-engineer/
│  ├─ web-video-presentation/
│  └─ xlsx/
├─ docs/
│  ├─ official-anthropic-skills.md
│  └─ skills-inventory.md
├─ setup-notes.md
└─ README.md
```

## 使用方式

- `prompts/global.md`：作为通用全局提示词使用。
- `prompts/github-repo-search.md`：用于让 AI 帮你从 GitHub 筛选 repo。
- `skills/`：放自定义或可迁移的 skill，尽量保持官方的“独立文件夹 + SKILL.md”结构。
- `docs/official-anthropic-skills.md`：已同步的官方 Anthropic skills 和安装命令。
- `setup-notes.md`：记录迁移、安装和配置注意事项。

## 迁移原则

- 提示词和 skill 尽量使用相对路径。
- 不把 API Key、账号密码、私人信息或公司机密写进仓库。
- 中文 Markdown 统一使用 UTF-8 编码。
- 如果包含敏感内容，优先使用私有仓库。
