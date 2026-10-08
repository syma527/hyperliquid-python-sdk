import allure
import pytest
import yaml
from pathlib import Path
import json


DATA_PATH = Path(__file__).resolve().parent / "data" / "hp_data.yaml"


def load_yaml():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"yaml文件不存在{DATA_PATH}")
    with open(DATA_PATH,'r',encoding="utf-8") as f:
        data=  yaml.safe_load(f)
    if not data:
        raise  ValueError(f"弹药库为空{DATA_PATH}")
    return data


@pytest.mark.parametrize("case_data",load_yaml())
def test_api_data_driven(api_client,case_data):
    #动态打标签
    allure.dynamic.feature(case_data.get("feature","未分类"))
    allure.dynamic.story(case_data.get("story","未分类"))
    allure.dynamic.title(case_data.get("case_name","未分类"))

    payload = case_data["payload"]
    # 把请求参数也放到报告中去,便于查找
    allure.attach(
        json.dumps(payload,ensure_ascii=False,indent=2),
        name="请求入参",
        attachment_type=allure.attachment_type.JSON
    )
    # 请求步骤
    with allure.step(f"POST /info 请求类型:{payload.get('type')}"):
        resp = api_client.post(endpoint="/info",json_data=payload)

    #把响应也加到报告中
    allure.attach(
        json.dumps(resp.json(),ensure_ascii=False,indent=2)[:3000],
        name="响应报文",
        attachment_type=allure.attachment_type.JSON
    )

    with allure.step(f"校验状态码 == {case_data['expected_status']}"):
        assert  resp.status_code == case_data['expected_status'],(
            f"用例[{case_data['case_name']}] 状态码异常,"
            f"预期{case_data['expected_status']},实际{resp.status_code}"
        )


