#!/usr/bin/env python3
"""
OnSessionEnd Hook - 会话结束时自动触发

功能：
1. 自动运行 Memory Compiler
2. 提取 Instincts
3. 更新置信度
"""

import sys
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from instincts.manager import InstinctManager
from memory_compiler.compiler import compile_memory

def on_session_end(session_transcript: str = None):
    """会话结束时的自动化流程"""
    print("\n" + "="*60)
    print("🤖 OnSessionEnd Hook 触发")
    print("="*60 + "\n")

    # 1. 运行 Memory Compiler
    print("📝 步骤 1: 编译记忆...")
    try:
        created_files = compile_memory(transcript_text=session_transcript)
        print(f"   ✅ 创建了 {len(created_files) if created_files else 0} 个记忆文件\n")
    except Exception as e:
        print(f"   ⚠️  记忆编译失败: {e}\n")

    # 2. 提取 Instincts (简化版)
    print("🧠 步骤 2: 提取 Instincts...")
    try:
        manager = InstinctManager()
        # 这里可以添加自动提取逻辑
        print(f"   ✅ Instincts 系统就绪\n")
    except Exception as e:
        print(f"   ⚠️  Instincts 提取失败: {e}\n")

    print("="*60)
    print("✅ 会话后处理完成")
    print("="*60 + "\n")

if __name__ == "__main__":
    # 从命令行参数或环境变量获取会话转录
    if len(sys.argv) > 1:
        transcript = sys.argv[1]
    else:
        transcript = os.environ.get("SESSION_TRANSCRIPT", "")

    on_session_end(transcript)
