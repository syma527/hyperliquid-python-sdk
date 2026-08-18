import pytest
import yaml
from pathlib import Path
import allure  # 🎯【全新导入】：大厂可视化报告的灵魂核心


def load_yaml():
    path_file = Path(__file__).parent
    data_path = path_file / 'data' / 'hp_data.yaml'
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# ====================================================
# 👑 Allure 皮肤管理层：给你的测试集合打上宏观标签
# ====================================================
@allure.feature("行情与风控资产管理中心")  # 史诗级大模块
@allure.story("交易所清算所状态快照全链路测试")  # 业务线场景
@pytest.mark.parametrize("yaml_info", load_yaml())
def test_api_load(api_client, yaml_info):
    c_name = yaml_info.get('case_name')
    payload = yaml_info.get("payload")
    expect_code = yaml_info.get("expected_status")

    # 🎯【动态用例标题】：让报告里的用例名字不再是死板的函数名，而是 yaml 里的 case_name 真实中文！
    allure.dynamic.title(f"DDT测试场景: {c_name}")

    # ====================================================
    # 🐾 Allure 步骤跟踪：把你的代码行变成报告里的“中文流水账”
    # ====================================================
    with allure.step("第一步：通过基础核心统一武器库发送请求"):
        # 在报告里附加本次发送的真实 Payload 快照， debug 时的逆天神器
        allure.attach(str(payload), name="本次发送的 Payload 弹药明细", attachment_type=allure.attachment_type.TEXT)
        response = api_client.post("/info", json_data=payload)

    with allure.get_status_expression() if False else allure.step("第二步：校验网络层通信状态码"):
        assert response.status_code == \
               expect_code, f"💥 状态码异常！实际为 {response.status_code}"

    with allure.step("第三步：进入风控解析，校验核心资产数据"):
        res_json = response.json()
        if "marginSummary" in res_json:
            actual_val = res_json['marginSummary'].get("accountValue")
            # 🎯 融入你刚刚攻克的金融强类型转换对齐，彻底免疫精度隐患
            assert float(actual_val) >= 0.0, f"💥 风控违规！全零地址总资产实际为: {actual_val}"
            # 把剥壳出来的核心数据，直接作为附件塞进 Allure 网页报告里供全组围观
            allure.attach(f"当前账户清算总价值: {actual_val}", name="风控数据审计快照",
                          attachment_type=allure.attachment_type.TEXT)

    print(f"🎉 用例 [{c_name}] 完美跑通！")
