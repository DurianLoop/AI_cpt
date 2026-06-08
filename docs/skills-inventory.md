# Skills Inventory

本仓库的 `skills/` 目录尽量遵循官方 skill 结构：每个 skill 是独立文件夹，并包含必需的 `SKILL.md`。

## 已收纳的个人 Skills

- `gpt-image-2`
- `kb-retriever`
- `web-design-engineer`
- `web-video-presentation`

## 已同步的 Anthropic 官方 Skills

来源：<https://github.com/anthropics/skills>

- `brand-guidelines`
- `claude-api`
- `docx`
- `frontend-design`
- `mcp-builder`
- `pdf`
- `pptx`
- `skill-creator`
- `theme-factory`
- `webapp-testing`
- `xlsx`

## 官方结构要点

每个 skill 推荐结构：

```text
skills/
└─ skill-name/
   ├─ SKILL.md
   ├─ scripts/
   ├─ references/
   └─ assets/
```

`SKILL.md` 顶部应包含 YAML frontmatter：

```yaml
---
name: skill-name
description: What this skill does, and when to use it.
---
```

## 迁移注意

- `skills/` 目录下尽量只放真正的 skill 文件夹。
- 不把 API Key、账号密码或私人信息写进 skill。
- 系统内置 skill 和插件缓存 skill 不建议重复迁移，目标环境通常会自动安装。
- 如果 skill 依赖外部命令、Python 包或 Node 包，迁移后需要重新安装依赖。
