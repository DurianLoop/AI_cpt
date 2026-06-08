# Setup Notes

这个文件用于记录把 AI 提示词和 skills 迁移到新电脑或新账号时需要做的事。

## 迁移清单

1. 克隆仓库

   ```powershell
   git clone https://github.com/DurianLoop/AI_cpt.git
   ```

2. 导入全局提示词

   使用 `prompts/global.md` 作为通用全局提示词。

3. 导入常用模板

   根据需要复制或引用 `prompts/` 目录下的任务模板。

4. 安装个人 skills

   检查 `skills/` 目录下每个 skill 的 `SKILL.md`，按说明安装。

   当前已收纳：

   - `gpt-image-2`
   - `kb-retriever`
   - `web-design-engineer`
   - `web-video-presentation`

5. 安装官方 Anthropic skills

   已同步清单和安装命令见：

   ```text
   docs/official-anthropic-skills.md
   ```

6. 配置环境变量

   如果某个 skill 需要 API Key 或账号信息，只在本机环境变量里配置，不写进仓库。

## 注意事项

- 仓库里只保存可迁移的提示词、模板、说明和 skill 文件。
- 敏感信息单独保存在本机或密码管理器里。
- 不写死本机绝对路径，例如 `C:\Users\...`。
- 中文文件统一使用 UTF-8 编码。
- `skills/` 目录尽量只放真正的 skill 文件夹，说明文档放到 `docs/`。
