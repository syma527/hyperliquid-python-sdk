# """
# 进阶题（容易踩坑）：特定币种参数精确校验
# 业务场景：去中心化交易所的币种参数（比如杠杆倍数、最小下单数量）绝对不能出错，否则会导致后续自动交易脚本疯狂报错。
#
# 具体要求：
#
# 同样请求 https://api.hyperliquid-testnet.xyz/info 的 {"type": "meta"} 接口。
#
# 拿到返回的 JSON 数据。
#
# 难点/易错点：你需要通过 Python 的循环或列表推导式，在 universe 列表中精确找到名字叫 "BTC" 的那个币种字典（注意：它不是死死固定在第一个位置的，前人写死下标 [0] 经常在公司里造成用例误报）。
#
# 找到 "BTC" 后，核心断言：断言 BTC 这个币种字典里，必须包含 "szDecimals"（尺寸精度）这个键（Key）。
#
# 3. 综合场景题：全链路“资产快照与风控校验”
# 业务场景：模拟用户在进行自动化结算时，风控系统需要拉取清算数据并验证极端行情下的参数。
#
# 具体要求：
#
# 本次请求的接口依然是测试网的 info 地址，但是请求体（Payload）变了。
#
# 请发送 POST 请求，Payload 改为：{"type": "clearinghouseState", "user": "0x0000000000000000000000000000000000000000"} （这是一个官方的公开全零测试地址，专用来查询空资产清算状态）。
#
# 核心校验链路：
#
# 先断言通信状态码为 200。
#
# 解析返回的 JSON。提取出返回数据中最外层的 "marginSummary"（保证金汇总）这个字典。
#
# 断言 "marginSummary" 字典里面的 "accountValue"（账户总价值）字段的值必须等于 "0.0"（因为我们查的是全零地址）。
#
# """
# """
#
# """
# import pytest
# import requests
#
# """def test_decimals():
#     url = "https://api.hyperliquid-testnet.xyz/info"
#     payload = {
#         "type":'meta'
#     }
#     headers=  {
#
#         "Content-Type": "application/json",
#         "User-Agent": "Apifox/1.0.0 (https://apifox.com)"
#
#     }
#     try:
#         response = requests.post(url=url,json=payload,headers=headers)
#         re_data = response.json()
#         res = [i for i in re_data["universe"] if i["name"] == "BTC"][0]
#         assert res.get('szDecimals',""),f"没有这个szDecimals这个key"
#
#         assert response.status_code == 200, f"状态码错误{response.status_code}"
#         #首先re_data 是个字典
#
#     except requests.exceptions.ConnectionError:
#         raise Exception("网络连接错误")"""
#
# """
# 进阶题（容易踩坑）：特定币种参数精确校验
# 业务场景：去中心化交易所的币种参数（比如杠杆倍数、最小下单数量）绝对不能出错，否则会导致后续自动交易脚本疯狂报错。
#
# 具体要求：
#
# 同样请求 https://api.hyperliquid-testnet.xyz/info 的 {"type": "meta"} 接口。
#
# 拿到返回的 JSON 数据。
#
# 难点/易错点：你需要通过 Python 的循环或列表推导式，在 universe 列表中精确找到名字叫 "BTC" 的那个币种字典（注意：它不是死死固定在第一个位置的，前人写死下标 [0] 经常在公司里造成用例误报）。
#
# 找到 "BTC" 后，核心断言：断言 BTC 这个币种字典里，必须包含 "szDecimals"（尺寸精度）这个键（Key）。
#
# 3. 综合场景题：全链路"资产快照与风控校验"
# 业务场景：模拟用户在进行自动化结算时，风控系统需要拉取清算数据并验证极端行情下的参数。
#
# 具体要求：
#
# 本次请求的接口依然是测试网的 info 地址，但是请求体（Payload）变了。
#
# 请发送 POST 请求，Payload 改为：{"type": "clearinghouseState", "user": "0x0000000000000000000000000000000000000000"} （这是一个官方的公开全零测试地址，专用来查询空资产清算状态）。
#
# 核心校验链路：
#
# 先断言通信状态码为 200。
#
# 解析返回的 JSON。提取出返回数据中最外层的 "marginSummary"（保证金汇总）这个字典。
#
# 断言 "marginSummary" 字典里面的 "accountValue"（账户总价值）字段的值必须等于 "0.0"（因为我们查的是全零地址）。
#
# """
# import requests
#
#
# def test_btc_decimals():
#     """测试 BTC 币种的 szDecimals 字段是否存在"""
#     url = "https://api.hyperliquid-testnet.xyz/info"
#     payload = {
#         "type": "meta"
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "User-Agent": "Apifox/1.0.0 (https://apifox.com)"
#     }
#     proxy = {
#         "http": "http://127.0.0.1:7897",
#         "https": "http://127.0.0.1:7897"
#     }
#
#     response = requests.post(
#         url=url,
#         headers=headers,
#         json=payload,
#         proxies=proxy,
#         timeout=10,
#         verify=False
#     )
#
#     assert response.status_code == 200, f"状态码错误{response.status_code}"
#
#     re_data = response.json()
#     universe_list = re_data.get("universe", [])
#
#     btc_matches = [coin for coin in universe_list if coin.get("name") == "BTC"]
#
#     assert len(btc_matches) > 0, "业务故障告警！从交易所接口返回的 universe 列表中未搜索到 BTC 资产！"
#
#     btc_coin = btc_matches[0]
#
#     assert "szDecimals" in btc_coin, "参数合规风控告警：BTC 币种字典中缺失核心下单精度字段 'szDecimals'！"
#



