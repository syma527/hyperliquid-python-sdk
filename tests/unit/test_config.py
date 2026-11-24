from tests.my_framework.common.config import resolve_base_url
from hyperliquid.utils.constants import TESTNET_API_URL,MAINNET_API_URL,LOCAL_API_URL




def test_local_url():

    assert resolve_base_url(env="local") == LOCAL_API_URL



def test_hl_env(monkeypatch):
    monkeypatch.setenv(name="HL_ENV",value='mainnet')
    assert resolve_base_url() == MAINNET_API_URL


def test_del_hl_env(monkeypatch):
