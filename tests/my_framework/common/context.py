# common/context.py
import json
from pathlib import Path
from typing import Any

class Context:
    """
    👑 大厂级上下文动态传递中间件
    1. 内存字典（单进程高速存取）
    2. 磁盘文件落盘（跨进程/多线程防丢失兜底）
    """
    _memory_store: dict[str, Any] = {}

    # 动态定位根目录下的临时上下文文件
    DB_FILE = Path(__file__).parent.parent / "outputs" / ".context_cache.json"
    print(DB_FILE)
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """存入动态上下文变量"""
        # 1. 写入内存
        cls._memory_store[key] = value

        # 2. 🛡️ 跨进程防御：同步写磁盘临时文件
        data = {}
        if cls.DB_FILE.exists():
            try:
                data = json.loads(cls.DB_FILE.read_text(encoding="utf-8"))
            except(json.JSONDecodeError,OSError):
                data = {}

        data[key] = value
        cls.DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        cls.DB_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """提取上下文变量"""
        # 优先读内存
        if key in cls._memory_store:
            return cls._memory_store[key]

        # 内存没有，去磁盘兜底读取
        if cls.DB_FILE.exists():
            try:
                data = json.loads(cls.DB_FILE.read_text(encoding="utf-8"))
                return data.get(key, default)
            except Exception:
                return default
        return default

if __name__ == '__main__':
    n = Context()
