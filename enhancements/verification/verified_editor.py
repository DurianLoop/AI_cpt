#!/usr/bin/env python3
"""
Hash-Verified File Editor - 哈希验证的文件编辑器

基于 hex-line 的设计，实现：
1. 编辑前后的哈希验证
2. 自动回滚机制
3. 编辑历史审计
"""

import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

class VerifiedEditor:
    """哈希验证的文件编辑器"""

    def __init__(self, audit_dir: str = "enhancements/verification/audit"):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def calculate_hash(self, content: str) -> str:
        """计算内容的 SHA-256 哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def verified_edit(self, file_path: str, old_content: str,
                     new_content: str) -> Tuple[bool, str]:
        """
        执行哈希验证的文件编辑

        Returns:
            (success, message)
        """
        filepath = Path(file_path)

        # 1. 备份原文件
        backup_path = self._create_backup(filepath)

        # 2. 验证原内容
        if filepath.exists():
            current_content = filepath.read_text(encoding='utf-8')
            current_hash = self.calculate_hash(current_content)
            expected_hash = self.calculate_hash(old_content)

            if current_hash != expected_hash:
                return False, (
                    f"❌ 文件已被修改！\n"
                    f"   当前哈希: {current_hash[:16]}...\n"
                    f"   期望哈希: {expected_hash[:16]}...\n"
                    f"   编辑前状态不匹配，已中止操作"
                )

        # 3. 执行编辑
        try:
            filepath.write_text(new_content, encoding='utf-8')
        except Exception as e:
            return False, f"❌ 写入失败: {e}"

        # 4. 验证编辑结果
        actual_content = filepath.read_text(encoding='utf-8')
        actual_hash = self.calculate_hash(actual_content)
        expected_new_hash = self.calculate_hash(new_content)

        if actual_hash != expected_new_hash:
            # 回滚
            shutil.copy(backup_path, filepath)
            return False, (
                f"❌ 编辑验证失败！\n"
                f"   实际哈希: {actual_hash[:16]}...\n"
                f"   期望哈希: {expected_new_hash[:16]}...\n"
                f"   已自动回滚到编辑前状态"
            )

        # 5. 记录审计日志
        self._log_edit(filepath, current_hash if filepath.exists() else "new",
                      actual_hash, success=True)

        return True, (
            f"✅ 编辑成功！\n"
            f"   文件: {filepath}\n"
            f"   新哈希: {actual_hash[:16]}...\n"
            f"   备份: {backup_path}"
        )

    def _create_backup(self, filepath: Path) -> Path:
        """创建备份文件"""
        if not filepath.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filepath.stem}_{timestamp}{filepath.suffix}.bak"
        backup_path = self.audit_dir / backup_name

        shutil.copy(filepath, backup_path)
        return backup_path

    def _log_edit(self, filepath: Path, old_hash: str,
                 new_hash: str, success: bool):
        """记录编辑日志"""
        log_file = self.audit_dir / "edit_log.jsonl"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file": str(filepath),
            "old_hash": old_hash,
            "new_hash": new_hash,
            "success": success
        }

        with open(log_file, 'a', encoding='utf-8') as f:
            import json
            f.write(json.dumps(log_entry) + '\n')

    def get_file_hash(self, file_path: str) -> Optional[str]:
        """获取文件的当前哈希值"""
        filepath = Path(file_path)
        if not filepath.exists():
            return None
        content = filepath.read_text(encoding='utf-8')
        return self.calculate_hash(content)

    def verify_file_integrity(self, file_path: str, expected_hash: str) -> bool:
        """验证文件完整性"""
        actual_hash = self.get_file_hash(file_path)
        return actual_hash == expected_hash if actual_hash else False

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python verified_editor.py hash <file>          # 获取文件哈希")
        print("  python verified_editor.py verify <file> <hash> # 验证文件完整性")
        sys.exit(1)

    editor = VerifiedEditor()
    command = sys.argv[1]

    if command == "hash" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        file_hash = editor.get_file_hash(file_path)
        if file_hash:
            print(f"SHA-256: {file_hash}")
        else:
            print("文件不存在")

    elif command == "verify" and len(sys.argv) >= 4:
        file_path = sys.argv[2]
        expected_hash = sys.argv[3]
        if editor.verify_file_integrity(file_path, expected_hash):
            print("✅ 文件完整性验证通过")
        else:
            print("❌ 文件完整性验证失败")

    else:
        print("参数错误")
