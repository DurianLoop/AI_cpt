#!/usr/bin/env python3
"""
自动配置增强系统

功能：
1. 检测环境
2. 配置 Hooks
3. 创建必要的目录
4. 验证安装
"""

import os
import json
import sys
from pathlib import Path

def setup_enhancements():
    print("🚀 AI_cpt 增强系统自动配置")
    print("="*60)

    # 1. 检测环境
    print("\n📋 步骤 1/4: 检测环境...")

    python_version = sys.version_info
    if python_version < (3, 7):
        print("❌ 需要 Python 3.7+，当前版本:", sys.version)
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}")

    # 2. 创建目录
    print("\n📁 步骤 2/4: 创建必要目录...")

    dirs = [
        "enhancements/instincts/data/active",
        "enhancements/instincts/data/evolved",
        "enhancements/verification/audit",
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path}")

    # 3. 配置 Hooks
    print("\n⚙️  步骤 3/4: 配置 Hooks...")

    claude_dir = Path.home() / ".claude"
    settings_file = claude_dir / "settings.json"

    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    else:
        settings = {}

    # 添加 Hook 配置
    current_dir = Path(__file__).parent.parent.absolute()
    hook_path = str(current_dir / "enhancements" / "hooks" / "on_session_end.py")

    if "hooks" not in settings:
        settings["hooks"] = {}

    settings["hooks"]["OnSessionEnd"] = {
        "command": "python",
        "args": [hook_path],
        "description": "自动编译记忆和提取 Instincts"
    }

    # 备份原配置
    if settings_file.exists():
        backup_file = settings_file.with_suffix(".json.backup")
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        print(f"   ✅ 已备份原配置到: {backup_file}")

    # 写入新配置
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)
    print(f"   ✅ 已更新: {settings_file}")

    # 4. 验证安装
    print("\n✔️  步骤 4/4: 验证安装...")

    # 测试 Instincts 管理器
    try:
        sys.path.insert(0, str(current_dir / "enhancements"))
        from instincts.manager import InstinctManager
        manager = InstinctManager()
        print("   ✅ Instincts 系统就绪")
    except Exception as e:
        print(f"   ⚠️  Instincts 系统警告: {e}")

    # 测试 Memory Compiler
    try:
        from memory_compiler.compiler import MemoryExtractor
        extractor = MemoryExtractor()
        print("   ✅ Memory Compiler 就绪")
    except Exception as e:
        print(f"   ⚠️  Memory Compiler 警告: {e}")

    # 测试哈希验证
    try:
        from verification.verified_editor import VerifiedEditor
        editor = VerifiedEditor()
        print("   ✅ 哈希验证系统就绪")
    except Exception as e:
        print(f"   ⚠️  哈希验证系统警告: {e}")

    print("\n" + "="*60)
    print("🎉 配置完成！")
    print("\n📖 下一步:")
    print("   1. 阅读 enhancements/INSTALL.md 了解详细用法")
    print("   2. 运行测试: python enhancements/instincts/manager.py list")
    print("   3. 开始使用 Claude Code，系统会自动学习")
    print("="*60)

    return True

if __name__ == "__main__":
    try:
        success = setup_enhancements()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 配置失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
