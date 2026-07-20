import pytest
import yaml
from pathlib import Path

#获取当前路径
current_file_path = Path(__file__).resolve().parent
file_dir = current_file_path / "data" / "new_data.yaml"

# 加载内容并抛出
def load_yaml():
    if not file_dir.exists():
        raise FileNotFoundError(f"找不到目标文件,请检查{file_dir}")

    with open(file=file_dir,mode='r',encoding="utf-8") as f:
        return yaml.safe_load(f)

#这里直接用参数解析解压
@pytest.mark.parametrize('yaml_info',load_yaml())
def test_xshop_login(yaml_info):
    #把数据从字典里面抠出来
    case_title = yaml_info["title"]
    input_user = yaml_info["user_input"]["username"]
    input_pwd = yaml_info["user_input"]["password"]
    expect_msg = yaml_info["expected"]

    print(f"流水线正在跑{case_title}")
    print(f"账号{input_user},密码{input_pwd}")
    if input_user == "admin" and input_pwd == "correct_password":
        actual_result = "登录成功"
    elif input_user == "wrong_user":
        actual_result = "账号不存在"
    else:
        actual_result = "密码错误"

    print(f"   -> [深度断言] 接口返回: '{actual_result}' == 预期: '{expect_msg}'")

    # 现代化 Pytest 原生纯净断言，有且仅有一记响亮的 assert！
    assert actual_result == expect_msg