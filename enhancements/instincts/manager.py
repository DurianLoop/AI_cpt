#!/usr/bin/env python3
"""
Instinct Manager - 管理和应用 Instincts

基于 ECC 的设计，实现：
1. Instinct 的 CRUD 操作
2. 置信度计算和更新
3. 进化检测和执行
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class Instinct:
    """Instinct 数据结构"""

    def __init__(self, name: str, content: str, confidence: float = 0.3,
                 instinct_type: str = "pattern", source: str = "observation"):
        self.name = name
        self.content = content
        self.confidence = confidence
        self.type = instinct_type
        self.source = source
        self.created = datetime.now().isoformat()
        self.last_verified = self.created
        self.verification_count = 0

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "content": self.content,
            "confidence": self.confidence,
            "type": self.type,
            "source": self.source,
            "created": self.created,
            "last_verified": self.last_verified,
            "verification_count": self.verification_count
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Instinct':
        inst = cls(data["name"], data["content"], data["confidence"],
                   data["type"], data["source"])
        inst.created = data.get("created", inst.created)
        inst.last_verified = data.get("last_verified", inst.last_verified)
        inst.verification_count = data.get("verification_count", 0)
        return inst

    def verify_success(self):
        """验证成功，增加置信度"""
        self.confidence = min(0.9, self.confidence + 0.1)
        self.verification_count += 1
        self.last_verified = datetime.now().isoformat()

    def verify_failure(self):
        """验证失败，降低置信度"""
        self.confidence = max(0.1, self.confidence - 0.2)
        self.last_verified = datetime.now().isoformat()

    def user_correction(self, new_content: str):
        """用户纠正，大幅提升置信度"""
        self.content = new_content
        self.confidence = min(0.9, self.confidence + 0.3)
        self.source = "user_correction"
        self.last_verified = datetime.now().isoformat()

    def should_evolve(self) -> bool:
        """判断是否应该进化为 Skill"""
        return self.confidence >= 0.9 and self.verification_count >= 3

class InstinctManager:
    """Instinct 管理器"""

    def __init__(self, data_dir: str = "enhancements/instincts/data"):
        self.data_dir = Path(data_dir)
        self.active_dir = self.data_dir / "active"
        self.evolved_dir = self.data_dir / "evolved"

        # 确保目录存在
        self.active_dir.mkdir(parents=True, exist_ok=True)
        self.evolved_dir.mkdir(parents=True, exist_ok=True)

    def save_instinct(self, instinct: Instinct) -> str:
        """保存 Instinct"""
        filepath = self.active_dir / f"{instinct.name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(instinct.to_dict(), f, indent=2, ensure_ascii=False)
        return str(filepath)

    def load_instinct(self, name: str) -> Optional[Instinct]:
        """加载 Instinct"""
        filepath = self.active_dir / f"{name}.json"
        if not filepath.exists():
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Instinct.from_dict(data)

    def list_instincts(self, min_confidence: float = 0.0) -> List[Instinct]:
        """列出所有 Instincts"""
        instincts = []
        for filepath in self.active_dir.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            inst = Instinct.from_dict(data)
            if inst.confidence >= min_confidence:
                instincts.append(inst)
        return sorted(instincts, key=lambda x: x.confidence, reverse=True)

    def evolve_instinct(self, name: str) -> bool:
        """将 Instinct 进化为 Skill"""
        instinct = self.load_instinct(name)
        if not instinct or not instinct.should_evolve():
            return False

        # 移动到 evolved 目录
        src = self.active_dir / f"{name}.json"
        dst = self.evolved_dir / f"{name}.json"
        src.rename(dst)

        print(f"✅ Instinct '{name}' 已进化！置信度: {instinct.confidence}")
        print(f"   建议创建对应的 Skill: skills/{name}/")
        return True

    def get_high_confidence_instincts(self) -> List[Instinct]:
        """获取高置信度的 Instincts（可直接应用）"""
        return self.list_instincts(min_confidence=0.7)


if __name__ == "__main__":
    import sys

    manager = InstinctManager()

    if len(sys.argv) < 2:
        print("用法: python manager.py [list|add|verify|evolve]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        instincts = manager.list_instincts()
        print(f"\n📚 共 {len(instincts)} 个 Instincts:\n")
        for inst in instincts:
            status = "🔥" if inst.confidence >= 0.7 else "📝"
            print(f"{status} {inst.name} (置信度: {inst.confidence:.1f}, 验证: {inst.verification_count}次)")
            print(f"   {inst.content[:60]}...")
            if inst.should_evolve():
                print(f"   ⚡ 可进化为 Skill！")
            print()

    elif command == "add" and len(sys.argv) >= 4:
        name = sys.argv[2]
        content = sys.argv[3]
        instinct = Instinct(name, content)
        manager.save_instinct(instinct)
        print(f"✅ 创建 Instinct: {name}")

    elif command == "verify" and len(sys.argv) >= 3:
        name = sys.argv[2]
        success = sys.argv[3].lower() == "success" if len(sys.argv) > 3 else True
        instinct = manager.load_instinct(name)
        if instinct:
            if success:
                instinct.verify_success()
            else:
                instinct.verify_failure()
            manager.save_instinct(instinct)
            print(f"✅ 更新置信度: {instinct.confidence:.1f}")
        else:
            print(f"❌ 未找到 Instinct: {name}")

    elif command == "evolve" and len(sys.argv) >= 3:
        name = sys.argv[2]
        if manager.evolve_instinct(name):
            print("进化成功！")
        else:
            print("进化失败：条件不满足或 Instinct 不存在")

    else:
        print("参数错误")

