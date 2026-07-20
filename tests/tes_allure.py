import allure
import yaml
import pytest
from pathlib import  Path

#导入yaml文件
PATH_FILE = Path(__file__).parent
PATH_YAML= PATH_FILE / 'data' / 'hp_data.yaml'
def loading_yaml():
    with open(file=PATH_YAML,mode = 'r',encoding='utf-8') as f:
        return yaml.safe_load(f)
@allure.epic("hyperliquid交易系统")
@allure.feature("行情与风控资产管理中心")
@allure.story("交易所清算所全链路测试")

@pytest.mark.parametrize("yaml_info",loading_yaml())
def test_api_load(api_client,yaml_info):
    c_name= yaml_info.get("case_name")
    payload= yaml_info.get("pay_load")
    expect_code= yaml_info.get("expected_status")

    allure.dynamic.title(f"DDT测试场景{c_name}")

    with allure.step("第一步,通过基础和兴统一发送请求"):
        allure.attach(str(payload),name="本次发送的Payload明细",attachment_type=)



if __name__ == '__main__':
    loading_yaml()
