from typing import Any


def assert_status(resp, expected: int = 200) -> None:
    """校验 HTTP 状态码；失败时附带响应体片段，方便定位"""
    assert resp.status_code == expected, (
        f"HTTP status mismatch: expected {expected}, got {resp.status_code}, "
        f"body: {resp.text[:200]}"
    )


def assert_key_in(data: dict, key: str) -> None:
    """校验字典包含指定 key；失败时列出实际所有 key"""
    assert key in data, f"missing key '{key}', actual keys: {sorted(data.keys())}"


def assert_not_empty(data: Any, name: str = "data") -> None:
    """校验集合非空；防'过滤过度/空返回'类假绿"""
    assert data, f"{name} should not be empty"