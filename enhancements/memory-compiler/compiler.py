#!/usr/bin/env python3
"""
Memory Compiler - Context Engineering 记忆编译器

基于 claude-memory-compiler 的设计，实现：
1. 从会话转录中提取关键信息
2. 语义理解和组织
3. 自动建立交叉引用
4. 突破 200 行限制
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

class MemoryExtractor:
    """从会话中提取记忆的 Agent"""

    def __init__(self):
        self.patterns = {
            "user_correction": r"(?:不是|应该是|其实是|纠正|改成)(.+)",
            "preference": r"(?:我喜欢|我偏好|我习惯|我想要)(.+)",
            "decision": r"(?:我们决定|确定使用|采用|选择)(.+)",
            "pattern": r"(?:每次|总是|通常|一般)(.+)",
            "lesson": r"(?:学到|发现|注意到|教训)(.+)",
        }

    def extract_from_session(self, transcript: str) -> List[Dict]:
        """从会话转录中提取记忆候选"""
        memories = []
        lines = transcript.split('\n')

        for i, line in enumerate(lines):
            # 跳过 system 和 assistant 消息，只关注 user
            if not line.startswith('user:'):
                continue

            content = line[5:].strip()

            # 检测各种模式
            for mem_type, pattern in self.patterns.items():
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    memories.append({
                        "type": mem_type,
                        "content": match.group(1).strip(),
                        "context": content,
                        "line_number": i,
                        "confidence": self._calculate_confidence(mem_type, content)
                    })

        return memories

    def _calculate_confidence(self, mem_type: str, content: str) -> float:
        """计算初始置信度"""
        base_confidence = {
            "user_correction": 0.9,  # 用户纠正最可靠
            "preference": 0.7,
            "decision": 0.8,
            "pattern": 0.5,
            "lesson": 0.6,
        }
        return base_confidence.get(mem_type, 0.5)

class MemorySynthesizer:
    """合成和组织记忆的 Agent"""

    def __init__(self, memory_dir: str = ".claude/projects/C--Users-Administrator/memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def synthesize(self, extracted_memories: List[Dict]) -> List[str]:
        """将提取的记忆合成为结构化文章"""
        # 按类型分组
        grouped = {}
        for mem in extracted_memories:
            mem_type = mem["type"]
            if mem_type not in grouped:
                grouped[mem_type] = []
            grouped[mem_type].append(mem)

        created_files = []

        for mem_type, memories in grouped.items():
            # 合并同类记忆
            merged_content = self._merge_memories(memories)
            if merged_content:
                filename = self._save_memory(mem_type, merged_content)
                created_files.append(filename)

        return created_files

    def _merge_memories(self, memories: List[Dict]) -> str:
        """合并同类记忆"""
        if not memories:
            return ""

        # 去重
        unique_contents = set(mem["content"] for mem in memories)
        avg_confidence = sum(mem["confidence"] for mem in memories) / len(memories)

        content_parts = []
        for content in unique_contents:
            content_parts.append(f"- {content}")

        return "\n".join(content_parts), avg_confidence

    def _save_memory(self, mem_type: str, merged_data) -> str:
        """保存记忆文件"""
        content, confidence = merged_data
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{mem_type}-{timestamp}.md"
        filepath = self.memory_dir / filename

        frontmatter = f"""---
name: {mem_type}-{timestamp}
type: {mem_type}
confidence: {confidence:.2f}
created: {datetime.now().isoformat()}
description: Auto-extracted from session
---

{content}

**How to apply**: 在相关场景下自动触发
**Confidence**: {confidence:.2f}
"""
        filepath.write_text(frontmatter, encoding='utf-8')
        return filename

class CrossReferencer:
    """建立交叉引用的 Agent"""

    def __init__(self, memory_dir: str = ".claude/projects/C--Users-Administrator/memory"):
        self.memory_dir = Path(memory_dir)

    def build_references(self):
        """构建记忆之间的引用"""
        all_memories = list(self.memory_dir.glob("*.md"))
        if not all_memories:
            return

        # 提取所有记忆的关键词
        memory_keywords = {}
        for mem_file in all_memories:
            content = mem_file.read_text(encoding='utf-8')
            keywords = self._extract_keywords(content)
            memory_keywords[mem_file.stem] = keywords

        # 建立引用关系
        for mem_file in all_memories:
            content = mem_file.read_text(encoding='utf-8')
            references = self._find_references(mem_file.stem, content, memory_keywords)

            if references:
                # 在文件末尾添加引用
                if "## 相关记忆" not in content:
                    content += "\n\n## 相关记忆\n\n"
                    for ref in references:
                        content += f"- [[{ref}]]\n"
                    mem_file.write_text(content, encoding='utf-8')

    def _extract_keywords(self, content: str) -> Set[str]:
        """提取关键词"""
        # 简单实现：提取常见技术词汇
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        return set(words)

    def _find_references(self, current_name: str, content: str,
                        all_keywords: Dict[str, Set[str]]) -> List[str]:
        """找到相关的记忆"""
        current_keywords = self._extract_keywords(content)
        references = []

        for name, keywords in all_keywords.items():
            if name == current_name:
                continue
            # 计算关键词重叠度
            overlap = len(current_keywords & keywords)
            if overlap >= 3:  # 至少 3 个共同关键词
                references.append(name)

        return references[:5]  # 最多 5 个引用


def compile_memory(transcript_path: str = None, transcript_text: str = None):
    """主编译流程"""
    print("🔍 Memory Compiler 启动...")

    # 1. 提取
    extractor = MemoryExtractor()
    if transcript_path:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
    elif transcript_text:
        transcript = transcript_text
    else:
        print("❌ 需要提供 transcript_path 或 transcript_text")
        return

    memories = extractor.extract_from_session(transcript)
    print(f"✅ 提取到 {len(memories)} 条记忆候选")

    # 2. 合成
    synthesizer = MemorySynthesizer()
    created_files = synthesizer.synthesize(memories)
    print(f"✅ 生成 {len(created_files)} 个记忆文件")

    # 3. 建立引用
    referencer = CrossReferencer()
    referencer.build_references()
    print(f"✅ 建立交叉引用完成")

    return created_files

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # 从文件读取
        compile_memory(transcript_path=sys.argv[1])
    else:
        # 从最近的会话读取
        history_file = Path.home() / ".claude" / "history.jsonl"
        if history_file.exists():
            print("📖 从最近的会话提取...")
            with open(history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    last_session = json.loads(lines[-1])
                    transcript = last_session.get("content", "")
                    compile_memory(transcript_text=transcript)
        else:
            print("❌ 未找到会话历史")

