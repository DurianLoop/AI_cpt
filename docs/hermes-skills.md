# Hermes / ClaudSkills

这里记录按用户图片清单同步的第三方 skills。

## 来源

- Hermes Agent: <https://github.com/NousResearch/hermes-agent>
- ClaudSkills creative-ideation: <https://claudskills.com/skills/creative-ideation/>

## 已同步

- `humanizer`：去 AI 味、增强文本真实语气。
- `claude-design`：一次性 HTML 设计产物，例如 landing、deck、prototype。
- `sketch`：快速做 2-3 个 HTML 设计草图用于比较。
- `research-paper-writing`：机器学习论文写作流程。
- `jupyter-live-kernel`：通过 live Jupyter kernel 做迭代 Python 分析。
- `plan`：规划模式，生成可执行 Markdown 计划。
- `powerpoint`：创建、读取、编辑 `.pptx`。
- `popular-web-designs`：参考真实设计系统做 HTML/CSS。
- `arxiv`：按关键词、作者、分类或 ID 搜索 arXiv。
- `ideation`：基于约束生成项目创意。

## 同步方式

```powershell
git -c http.proxy=http://127.0.0.1:7897 -c https.proxy=http://127.0.0.1:7897 clone https://github.com/NousResearch/hermes-agent.git work\hermes-agent

Copy-Item -Recurse -Force work\hermes-agent\skills\creative\humanizer skills\humanizer
Copy-Item -Recurse -Force work\hermes-agent\skills\creative\claude-design skills\claude-design
Copy-Item -Recurse -Force work\hermes-agent\skills\creative\sketch skills\sketch
Copy-Item -Recurse -Force work\hermes-agent\skills\research\research-paper-writing skills\research-paper-writing
Copy-Item -Recurse -Force work\hermes-agent\skills\data-science\jupyter-live-kernel skills\jupyter-live-kernel
Copy-Item -Recurse -Force work\hermes-agent\skills\software-development\plan skills\plan
Copy-Item -Recurse -Force work\hermes-agent\skills\productivity\powerpoint skills\powerpoint
Copy-Item -Recurse -Force work\hermes-agent\skills\creative\popular-web-designs skills\popular-web-designs
Copy-Item -Recurse -Force work\hermes-agent\skills\research\arxiv skills\arxiv

New-Item -ItemType Directory -Force -Path skills\ideation
Invoke-WebRequest -Uri https://claudskills.com/skills/creative-ideation/SKILL.md -OutFile skills\ideation\SKILL.md
```
