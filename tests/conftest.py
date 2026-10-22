"""
设置全局
"""
import time

import allure
from tests.my_framework.tools.my_log import log
from tests.my_framework.common.config import resolve_base_url
import pytest
from tests.my_framework.common.api_client import ApiClient
from pathlib import  Path
from tests.my_framework.common.infoapi import InfoApi
from tests.my_framework.tools.redact import redact_text

#adoption方法把写好的环境值读出来,--env,default = None 是如果用户没给,就为空,走默认,为空的话,才能自己输入

def pytest_addoption(parser):
    """为什么要这个函数,因为有了他可以命令行指定配置环境"""
    parser.addoption(
        "--env",
        default=None,
        help="testnet/local/mainnet（默认 testnet）"
    )

@pytest.fixture(scope="session")
def base_url(request) -> str:

    url=  resolve_base_url(request.config.getoption("--env"))
    log.info(f"本次运行环境:{url}")
    return url


@pytest.fixture(scope="session")

def api_client(base_url):
    log.info("设置全局api客户端,省略重复请求,只在这一块设置就好了")
    client = ApiClient(base_url=base_url)
    yield client

    log.info("会话结束,关闭连接池")
    client.session.close()




@pytest.hookimpl(tryfirst=True,hookwrapper=True)
def pytest_runtest_makereport(item,call):
    """用例失败,自动把日志贴进allure报告"""

    outcome = yield
    # 拿到结果后,拆解结果
    result = outcome.get_result()
    if result.failed:
        today = time.strftime("%Y_%m_%d")
        log_file = (
            Path(__file__).resolve().parent / "my_framework" / "logs" / f"{today}.log"
        )

        if log_file.exists():
            content = log_file.read_text(encoding="utf-8")
            content = content[-2000:]
            content = redact_text(content)
            allure.attach(
                content,
                name=f"失败日志{item.name}",
                attachment_type=allure.attachment_type.TEXT,
            )


@pytest.fixture(scope="session")
def info_api(api_client):
    """提供 /info 的业务语义封装实例"""
    return InfoApi(api_client)

