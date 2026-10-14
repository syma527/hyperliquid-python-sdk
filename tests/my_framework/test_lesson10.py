import allure
from tests.my_framework.common.assert_common import assert_key_in, assert_not_empty
from pathlib import Path
import yaml
import pytest
from tests.my_framework.test_lesson08 import load_yaml

DATA_PATH = Path(__file__).resolve().parent / "data" / "user_address.yaml"

address_res = load_yaml(DATA_PATH)


@allure.feature("接口封装层")
@allure.story("元数据")
def test_meta_returns_universe(info_api):
    """meta() 应返回含 universe 的字典"""
    allure.dynamic.title("meta 返回 universe")
    result = info_api.meta()
    assert_key_in(result, key="universe")


@allure.feature("接口封装层")
@allure.story("账户状态")
@pytest.mark.parametrize("data", address_res, ids=lambda d: d["name"])
def test_clearinghouse_state_returns_margin_summary(info_api, data):
    """clearinghouse_state() 应返回含 marginSummary 的账户状态"""
    allure.dynamic.title(f"clearinghouse_state 返回 marginSummary --{data['name']}")
    user_address = data["user_address"]
    state = info_api.clearinghouse_state(address=user_address)

    assert_key_in(state, key="marginSummary")


@allure.feature("接口封装层")
@allure.story("perp_mids接口返回")
def test_perp_mids(info_api):
    allure.dynamic.title("pers_mids返回永续报价")
    mids = info_api.perp_mids()
    assert mids, "perp mids should not be empty"
    assert all(not k.startswith(("@", "#")) for k in mids), "perp mids should exclude spot keys "

    assert_key_in(mids, key="BTC")
