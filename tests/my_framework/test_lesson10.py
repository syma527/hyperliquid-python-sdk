import allure


@allure.feature("接口封装层")
@allure.story("元数据")
def test_meta_returns_universe(info_api):
    """meta() 应返回含 universe 的字典"""
    allure.dynamic.title("meta 返回 universe")
    result = info_api.meta()
    assert "universe" in result, "meta response missing universe"


@allure.feature("接口封装层")
@allure.story("账户状态")
def test_clearinghouse_state_returns_margin_summary(info_api):
    """clearinghouse_state() 应返回含 marginSummary 的账户状态"""
    allure.dynamic.title("clearinghouse_state 返回 marginSummary")
    user_address = "0x7237452d6A4d8D8B7B32A83868E82A1eBf1d58ce"
    state = info_api.clearinghouse_state(address=user_address)
    assert isinstance(state, dict), "clearinghouse state should be a dict"
    assert "marginSummary" in state, "clearinghouse state missing marginSummary"