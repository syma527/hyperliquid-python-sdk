import os

from hyperliquid.utils.constants import TESTNET_API_URL,LOCAL_API_URL,MAINNET_API_URL
#定义一个默认环境
DEFAULT_ENV = "testnet"

ENV_MAP= {
    "testnet": TESTNET_API_URL,
    "local": LOCAL_API_URL,
    "mainnet": MAINNET_API_URL,
}


def resolve_base_url(env:str|None=None)-> str:
    name = env or os.environ.get("HL_ENV",DEFAULT_ENV)

    if name not in ENV_MAP:
        raise ValueError(f"not find this {name} in {sorted(ENV_MAP)}")

    return  ENV_MAP[name]

