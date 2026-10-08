"""
设置全局
"""
import time

import allure
from tests.my_framework.tools.my_log import log
from hyperliquid.utils.constants import TESTNET_API_URL
import pytest
from tests.my_framework.common.api_client import ApiClient
from pathlib import  Path
from tests.my_framework.common.infoapi import InfoApi

@pytest.fixture(scope="session")
def api_client():
    log.info("设置全局api客户端,省略重复请求,只在这一块设置就好了")
    client = ApiClient(base_url=TESTNET_API_URL)
    yield client

    log.info("会话结束,关闭连接池")
    client.session.close()



@pytest.hookimpl(tryfirst=True,hookwrapper=True)

def pytest_runtest_makereport(item,call):
    """用例失败,自动把日志贴进allure报告"""

    outcome = yield

    result = outcome.get_result()

    if result.failed:
        today = time.strftime("%Y_%m_%d")
        log_file = (
            Path(__file__).resolve().parent / "my_framework" / "logs" / f"{today}.log"
        )

        if log_file.exists():
            content = log_file.read_text(encoding="utf-8")
            content = content[-2000:]

            allure.attach(
                content,
                name=f"失败日志{item.name}",
                attachment_type=allure.attachment_type.TEXT,
            )






@pytest.fixture(scope="session")
def info_api(api_client):
    """提供 /info 的业务语义封装实例"""
    return InfoApi(api_client)

