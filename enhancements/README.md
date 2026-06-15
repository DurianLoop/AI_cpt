# 增强系统总览

本目录包含从 GitHub 热门仓库集成的三大核心功能。

## 🎯 集成来源

| 系统 | 灵感来源 | Stars | 核心价值 |
|------|----------|-------|----------|
| Instincts | [ECC](https://github.com/affaan-m/ecc) | 215K+ | 自动学习系统 |
| Memory Compiler | [claude-memory-compiler](https://github.com/coleam00/claude-memory-compiler) | 1.2K+ | Context Engineering |
| Hash Verification | [claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) | 492+ | 编辑可靠性保障 |

## 📁 模块说明

### 1. instincts/ - Instincts 学习系统

**功能**：
- 原子级学习单元，比 Skills 更细粒度
- 置信度评分机制（0.3-0.9）
- 自动从会话中提取模式
- 高置信度 Instincts 可进化为 Skills

**关键文件**：
- `manager.py`：Instinct 管理器
- `data/active/`：活跃的 Instincts
- `data/evolved/`：已进化的 Instincts

**使用场景**：
- 捕获用户的重复偏好
- 自动学习项目特定的模式
- 减少手动配置工作

### 2. memory-compiler/ - Context Engineering

**功能**：
- 自动从会话中提取关键信息
- 语义理解（不只是关键词匹配）
- 自动建立记忆间的交叉引用
- 突破原生 200 行 + 25KB 限制

**关键文件**：
- `compiler.py`：记忆编译器主程序

**使用场景**：
- 会话结束后自动整理记忆
- 从大量会话中提炼知识
- 建立知识图谱

### 3. verification/ - 哈希验证系统

**功能**：
- 编辑前后的 SHA-256 哈希验证
- 验证失败自动回滚
- 完整的审计日志

**关键文件**：
- `verified_editor.py`：验证编辑器
- `audit/`：审计日志和备份

**使用场景**：
- 编辑重要配置文件
- 防止上下文错误导致的文件损坏
- 需要审计追踪的操作

### 4. hooks/ - 自动化触发器

**功能**：
- OnSessionEnd：会话结束时自动运行
- 集成 Memory Compiler 和 Instincts 提取

**关键文件**：
- `on_session_end.py`：会话结束 Hook

**配置方法**：
在 `.claude/settings.json` 中添加：
```json
{
  "hooks": {
    "OnSessionEnd": {
      "command": "python",
      "args": ["enhancements/hooks/on_session_end.py"]
    }
  }
}
```

## 🚀 快速配置

### 最小化配置（5 分钟）

1. 复制 `config.json` 到 `.claude/settings.json` 并合并
2. 测试 Instincts 管理器：
   ```bash
   python enhancements/instincts/manager.py list
   ```

### 完整配置（15 分钟）

1. 完成最小化配置
2. 配置 OnSessionEnd Hook
3. 手动运行一次 Memory Compiler 测试
4. 创建第一个 Instinct 并验证

## 📊 效果对比

| 功能 | 原生方案 | 增强后 |
|------|----------|--------|
| 记忆管理 | 手动编写，200 行限制 | 自动提取，无限制 |
| 学习能力 | 静态配置 | 动态学习 + 进化 |
| 编辑可靠性 | 无验证 | 哈希验证 + 回滚 |
| 记忆检索 | 关键词匹配 | 语义理解 |

## 🔗 相关文档

- [Instincts 系统详细说明](instincts/README.md)
- [Claude Code 热门仓库深度分析](../Claude_Code_热门仓库深度实现分析.md)
- [ECC 官方文档](https://affaan-m-everything-claude-code.mintlify.app)
- [Memory Compiler 设计](https://github.com/coleam00/claude-memory-compiler)

## 💡 最佳实践

1. **Instincts 管理**：
   - 定期检查高置信度的 Instincts
   - 及时进化成 Skills
   - 删除过时的 Instincts

2. **Memory Compiler**：
   - 让它在后台自动运行
   - 定期检查生成的记忆文件
   - 手动补充重要上下文

3. **哈希验证**：
   - 对重要文件启用验证
   - 保留审计日志
   - 定期清理旧备份

## 🛠️ 故障排查

**Q: Instincts 不自动提取？**
- 检查 OnSessionEnd Hook 是否配置
- 确认 Python 路径正确
- 查看 `.claude/` 日志

**Q: Memory Compiler 提取不准确？**
- 调整 `compiler.py` 中的模式匹配
- 增加关键词
- 手动补充提取结果

**Q: 哈希验证总是失败？**
- 检查文件编码（应为 UTF-8）
- 确认没有其他进程修改文件
- 查看审计日志定位问题

## 📈 未来路线图

- [ ] 集成更多 ECC 的 Agents
- [ ] 实现 hex-graph 代码知识图谱
- [ ] 支持团队共享 Instincts
- [ ] Web UI 管理界面
- [ ] 统计和可视化仪表板
