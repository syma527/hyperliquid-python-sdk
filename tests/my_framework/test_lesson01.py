import requests
def test_meta_contains_btc():
    resp = requests.post(
        "https://api.hyperliquid-testnet.xyz/info",
        json={"type": "meta"},
        timeout=10,
    )

    # ① 通信断言：状态码
    assert resp.status_code == 200, f"实际状态码为{resp.status_code}"
    resp_json = resp.json()
    # ② 结构断言：universe 存在且非空（会变，不断具体数量）
    assert "universe" in resp_json,f"meta必须包含universe字段,实际字段为{list(resp_json.keys())}"
    assert len(resp_json["universe"]) > 0,f"universe 为空"
    # ③ 业务断言：找到 BTC，校验核心字段
    btc_list = [i for i in resp_json["universe"] if i["name"] == "BTC"]
    assert len(btc_list)>0,"btc 不存在"
    btc = btc_list[0]
    # ④ 精度字段：类型对 + 值合理（重点：带上实际值）
    assert btc["szDecimals"] == 5,f"btc的精度不对,实际精度为{btc['szDecimals']}"
