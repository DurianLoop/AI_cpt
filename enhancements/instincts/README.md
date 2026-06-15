# Instincts 系统

> 基于 ECC (Everything Claude Code) 的原子级学习系统

## 核心概念

Instincts 是比 Skills 更细粒度的"本能"行为单元，具有以下特性：

- **原子级**：每个 Instinct 只包含一个最小的可学习行为
- **置信度评分**：0.3-0.9，表示该行为的可靠性
- **自动提取**：从会话中自动学习，无需手动编写
- **可进化**：高置信度的 Instinct 可以进化为 Skill

## 文件格式

```markdown
---
name: git-commit-style
type: instinct
confidence: 0.8
created: 2026-06-15
last_verified: 2026-06-15
verification_count: 5
source: user_correction
---

用户偏好简短的 commit message（<50 字符）。

**Why**: 方便查看 git log 一行模式
**How to apply**: 写 commit 前自动检查长度
**Evolution path**: confidence >= 0.9 → git-workflow skill
```

## 置信度计算规则

| 事件 | 置信度变化 |
|------|------------|
| 首次观察 | 0.3 |
| 验证成功 | +0.1 |
| 用户明确纠正 | +0.3 |
| 重复出现 3+ 次 | +0.2 |
| 验证失败 | -0.2 |

## 进化路径

```
Instinct (0.3) → 观察期
    ↓
Instinct (0.6) → 验证期
    ↓
Instinct (0.8) → Skill 候选
    ↓
Skill → 正式技能
```

## 使用方法

1. 会话中正常工作
2. 系统自动捕获模式
3. 查看生成的 instincts 文件
4. 高置信度的自动应用

## 目录结构

```
instincts/
├── README.md           # 本文档
├── manager.py          # Instinct 管理器
├── extractor.py        # 自动提取器
├── data/               # Instinct 数据存储
│   ├── active/         # 活跃的 Instincts
│   └── evolved/        # 已进化的 Instincts
└── templates/          # Instinct 模板
```
