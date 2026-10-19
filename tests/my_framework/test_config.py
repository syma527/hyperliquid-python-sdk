import pytest

from hyperliquid.utils.constants import MAINNET_API_URL, TESTNET_API_URL
from tests.my_framework.common.config import ENV_MAP, resolve_base_url


def test_resolve_explicit_env_wins():
    """命令行传入的 --env 优先级最高"""
    assert resolve_base_url("mainnet") == MAINNET_API_URL


def test_env_var_takes_effect(monkeypatch):
    """没有显式参数时，读取 HL_ENV 环境变量"""
    monkeypatch.setenv("HL_ENV", "mainnet")
    assert resolve_base_url() == MAINNET_API_URL


def test_default_is_testnet_when_nothing_set(monkeypatch):
    """什么都没指定时，落到安全默认值 testnet"""
    monkeypatch.delenv("HL_ENV", raising=False)
    assert resolve_base_url() == TESTNET_API_URL


def test_unknown_env_fails_fast():
    """未知环境必须当场报错，不允许悄悄兜底"""
    with pytest.raises(ValueError, match="staging"):
        resolve_base_url("staging")


def test_base_url_fixture_is_known_environment(base_url):
    assert base_url in ENV_MAP.values()