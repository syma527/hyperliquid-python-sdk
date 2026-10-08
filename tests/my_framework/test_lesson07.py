import allure
import pytest

@allure.feature("行情接口")
@allure.story("获取元数据")
def test_meta_has_universe_field(api_client):
    """
    用例描述:验证meta 接口返回包含 universe 字段
    """

    resp = api_client.post(endpoint="/info",json_data={"type":"meta"})

    assert resp.status_code == 200,"HTTP 状态码异常"
    assert "universe" in resp.json(),"缺少 universe 字段"

@allure.feature("行情接口")
@allure.story("查询实时价格")
def test_all_mids_returns(api_client):
    resp = api_client.post(endpoint="/info",json_data={"type":"allMids"})

    assert  resp.status_code == 200
    data = resp.json()
    #allure step: 把关键步骤记录下来,报告里能看到执行过程
    with allure.step("检查BTC 是否存在于字典"):
        has_btc = "BTC" in data

    assert has_btc,"返回中找不到BTC 价格"

@allure.feature("资产快照")
@allure.story("查询用户资产")

def test_user_state_success(api_client):

    test_address = "0x0000000000000000000000000000000000000000"

    with allure.step(f"请求{test_address}的账户状态"):
        resp = api_client.post(
            endpoint="/info",
            json_data={"type": "clearinghouseState", "user": test_address},
        )

        assert resp.status_code == 200
        result = resp.json()

        # 断言核心字段存在
    with allure.step("校验返回结构包含 marginSummary"):
        assert "marginSummary" in result, "缺少 marginSummary 字段"




