# 增强系统安装指南

## 📦 系统要求

- Python 3.7+
- Claude Code CLI
- Git

## 🚀 快速安装

### 步骤 1：克隆仓库

```bash
git clone https://github.com/DurianLoop/AI_cpt.git
cd AI_cpt
```

### 步骤 2：配置增强系统

#### 方案 A：自动配置（推荐）

```bash
# Windows
python enhancements\setup.py

# Linux/Mac
python enhancements/setup.py
```

#### 方案 B：手动配置

1. **配置 Hooks**

编辑 `~/.claude/settings.json`，添加：

```json
{
  "hooks": {
    "OnSessionEnd": {
      "command": "python",
      "args": ["/path/to/AI_cpt/enhancements/hooks/on_session_end.py"],
      "description": "自动编译记忆和提取 Instincts"
    }
  }
}
```

2. **测试 Instincts 系统**

```bash
cd AI_cpt
python enhancements/instincts/manager.py list
```

3. **测试 Memory Compiler**

```bash
python enhancements/memory-compiler/compiler.py
```

### 步骤 3：验证安装

```bash
# 创建测试 Instinct
python enhancements/instincts/manager.py add test-instinct "这是测试"

# 查看列表
python enhancements/instincts/manager.py list

# 验证成功
python enhancements/instincts/manager.py verify test-instinct success

# 再次查看（置信度应该提升）
python enhancements/instincts/manager.py list
```

## 📖 使用示例

### 1. Instincts 工作流

```bash
# 场景：发现用户喜欢简短的 commit message

# 1. 创建 Instinct
python enhancements/instincts/manager.py add git-commit-style "用户偏好 <50 字符的 commit message"

# 2. 每次应用成功后验证
python enhancements/instincts/manager.py verify git-commit-style success

# 3. 多次验证后，置信度到达 0.9，可以进化
python enhancements/instincts/manager.py evolve git-commit-style

# 4. 基于进化的 Instinct 创建正式 Skill
```

### 2. Memory Compiler 工作流

```bash
# 会话结束后自动运行（如果配置了 Hook）
# 或手动运行：
python enhancements/memory-compiler/compiler.py

# 查看生成的记忆
ls ~/.claude/projects/*/memory/
```

### 3. 哈希验证工作流

```python
# 在你的脚本中使用
from enhancements.verification.verified_editor import VerifiedEditor

editor = VerifiedEditor()

# 获取文件哈希
original_hash = editor.get_file_hash("config.json")
print(f"原始哈希: {original_hash}")

# 执行验证编辑
old_content = open("config.json").read()
new_content = old_content.replace("old", "new")

success, message = editor.verified_edit(
    "config.json",
    old_content,
    new_content
)

print(message)
```

## 🎯 实际场景

### 场景 1：自动学习 Git 工作流偏好

```bash
# 你在对话中多次提到喜欢用 conventional commits
# OnSessionEnd Hook 自动提取 Instinct
# 几次验证后，自动应用到后续的 commit message 生成
```

### 场景 2：积累项目特定知识

```bash
# 你在多个会话中讨论了项目的架构决策
# Memory Compiler 自动提取并组织成知识文章
# 建立交叉引用，方便后续查找
```

### 场景 3：保护重要配置文件

```python
# 编辑 .env 或其他重要配置时
# 使用 VerifiedEditor 确保编辑正确
# 失败自动回滚，有审计日志
```

## ⚙️ 高级配置

### 调整 Instincts 阈值

编辑 `enhancements/config.json`：

```json
{
  "settings": {
    "enhancements": {
      "instincts": {
        "min_confidence_to_apply": 0.7,  // 调低更积极，调高更保守
        "evolution_threshold": 0.9        // 进化所需的置信度
      }
    }
  }
}
```

### 自定义记忆提取模式

编辑 `enhancements/memory-compiler/compiler.py` 中的 `patterns` 字典：

```python
self.patterns = {
    "user_correction": r"(?:不是|应该是|其实是|纠正|改成)(.+)",
    "preference": r"(?:我喜欢|我偏好|我习惯|我想要)(.+)",
    "decision": r"(?:我们决定|确定使用|采用|选择)(.+)",
    # 添加你自己的模式
    "custom_pattern": r"你的正则表达式"
}
```

## 🐛 故障排查

### 问题：Hook 不触发

**检查清单**：
1. `settings.json` 路径是否正确（绝对路径）
2. Python 命令是否在 PATH 中
3. 查看 `.claude/` 目录下的日志

**解决方案**：
```bash
# 测试 Hook 能否手动运行
python /path/to/AI_cpt/enhancements/hooks/on_session_end.py "test"
```

### 问题：Instincts 不自动提取

**原因**：
- OnSessionEnd Hook 未配置
- 会话内容不匹配提取模式

**解决方案**：
1. 手动创建 Instinct 测试系统
2. 调整提取模式
3. 检查会话历史格式

### 问题：Memory Compiler 提取不准确

**解决方案**：
1. 调整 `compiler.py` 中的正则表达式
2. 增加或修改提取模式
3. 手动补充遗漏的记忆

## 📚 延伸阅读

- [Instincts 系统详解](instincts/README.md)
- [增强系统总览](README.md)
- [Claude Code 热门仓库分析](../Claude_Code_热门仓库深度实现分析.md)
- [ECC 官方文档](https://affaan-m-everything-claude-code.mintlify.app)

## 💬 获取帮助

- 查看 [GitHub Issues](https://github.com/DurianLoop/AI_cpt/issues)
- 阅读 [故障排查指南](#故障排查)
- 参考 [使用示例](#使用示例)

## 🎉 下一步

安装完成后，建议：

1. ✅ 创建几个测试 Instincts，熟悉工作流
2. ✅ 配置 OnSessionEnd Hook，实现自动化
3. ✅ 在实际项目中使用，观察效果
4. ✅ 定期检查生成的 Instincts 和记忆
5. ✅ 根据需求调整配置参数

Happy coding! 🚀
