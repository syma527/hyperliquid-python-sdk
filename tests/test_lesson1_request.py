import pytest
from tests.common.api_client import ApiClient


# ====================================================
# 🧭 1. 定义共享单车（Fixture 前置初始化）
# ====================================================
@pytest.fixture(scope="session")
def api_client():
    """
    创建一个全局共享的 ApiClient 实例。
    scope="session" 代表整个测试过程中，这辆车只会被实例化创造一次，所有用例共享，极度节省内存！
    """
    print("\n📦 [Fixture] 正在为你全球初始化大厂级 ApiClient 客户端...")
    client = ApiClient(base_url="https://api.hyperliquid-testnet.xyz")
    return client


# ====================================================
# 🧪 2. 极其干净、纯粹的业务测试用例层
# ====================================================
#
# def test_btc_decimals(api_client):
#     """ 精准校验btc的szdecimal字段"""
#     #重点看这个脚本名字里面的api_client
#     payload = {}

def test_user_margin_snapshot(api_client):
    """【重构第三题】：全链路资产快照与风控校验"""
    # 🎯 亮点：同样直接高空召唤 api_client，不需要重新初始化任何网络配置
    payload = {
        "type": "clearinghouseState",
        "user": "0x0000000000000000000000000000000000000000"
    }

    # 直接调用，极其丝滑
    response = api_client.post("/info", json_data=payload)

    assert response.status_code == 200, f"状态码错误: {response.status_code}"

    res_data = response.json()
    margin_summary = res_data.get("marginSummary", {})
    actual_account_value = margin_summary.get("accountValue")

    # 牢记你上一课攻克的字符串类型深坑
    assert actual_account_value >= "0.0", f"风控违规！实际为: {actual_account_value}"
    print(f" -> 全零地址资产风控校验 Passed!")

def test_timeout(api_client):
    payload = {
        "type":"meta"
    }
    response = api_client.post("/info",payload)
    assert response.status_code == 200,f"状态码实际是{response.status_code}"
    res_data = response.json()
    print("\n正在检查接口健康度")
    assert response.elapsed.total_seconds() <2.5,f"响应超时"

