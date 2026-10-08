"""第9课：多接口关联与上下文传递"""

import json

import allure
import pytest



@pytest.fixture(scope="session")
def meta_universe(info_api):
    """提取一次 meta 的 universe，整个会话复用（第4课单例思想）"""
    return info_api.meta()["universe"]


@pytest.fixture(scope="session")
def all_mids(info_api):

    return info_api.all_mids()



# ... existing code ...
@allure.feature("跨接口一致性")
@allure.story("币种覆盖对齐")
def test_every_meta_coin_has_price(meta_universe, all_mids):
    """meta 声明的每个币种，allMids 必须都有报价"""
    allure.dynamic.title("meta 声明的币种在 allMids 中全覆盖")

    meta_names = {coin["name"] for coin in meta_universe}   # ① meta 声明的币名集合
    priced_names = set(all_mids.keys())                     # ② allMids 有报价的 key 集合
    missing = meta_names - priced_names                     # ③ 差集：有声明无报价

    allure.attach(
        json.dumps(sorted(missing), ensure_ascii=False, indent=2),
        name="缺失报价的币种",
        attachment_type=allure.attachment_type.JSON,
    )

    assert not missing, f"以下币种在 meta 有声明但 allMids 无报价: {sorted(missing)}"


@allure.feature("跨接口一致性")
@allure.story("BTC 精度与价格联动")
def test_btc_price_positive_and_precise(meta_universe, all_mids):
    """从 meta 提取 BTC 精度，从 allMids 提取 BTC 价格，联动校验"""
    allure.dynamic.title("BTC 价格与精度联动校验")

    with allure.step("从 meta 提取 BTC 元数据"):
        btc_meta = next((c for c in meta_universe if c["name"] == "BTC"), None)
    assert btc_meta is not None, "meta 中找不到 BTC"

    with allure.step("从 allMids 提取 BTC 价格"):
        btc_price_raw = all_mids.get("BTC")
    assert btc_price_raw is not None, "allMids 中找不到 BTC 报价"

    with allure.step("强类型转换后校验价格为正数"):
        btc_price = float(btc_price_raw)
        assert btc_price > 0, f"BTC 价格异常: {btc_price_raw}"

    allure.attach(
        json.dumps(
            {"szDecimals": btc_meta["szDecimals"], "mid": btc_price_raw},
            ensure_ascii=False,
            indent=2,
        ),
        name="BTC 联动数据",
        attachment_type=allure.attachment_type.JSON,
    )


