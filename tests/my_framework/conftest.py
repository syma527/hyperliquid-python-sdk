# tests/conftest.py 文件的完全体

import allure
import pytest
from tests.my_framework.tools.handle_logs import create_logger
from tests.my_framework.common.api_client import ApiClient
log = create_logger("XHOP")
@pytest.fixture(scope="session")
def api_client():
    """
    整个测试生命周期内，有且仅实例化创建一次的全局 ApiClient 单例客户端。
    """
    print("\n📦 [后勤基建] 全局单例 ApiClient 物流车已由 conftest 成功派遣...")
    # 传入你第一课、第二课封装好的武器库，指定基础域名环境
    client = ApiClient(base_url="https://api.hyperliquid-testnet.xyz")
    yield client
    print("收到熔断信号,全自动触发数据销毁与session会话安全关闭")
# 失败时候截图

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    🎯 监听 Pytest 用例生命周期的每一个阶段
    """
    # 1. 执行常规流程，让 Pytest 产生测试报告结果
    outcome = yield
    report = outcome.get_result()

    # 2. 只有当用例在 'call' (真正运行测试代码) 阶段发生失败时才触发拦截
    if report.when == "call" and report.failed:
        # -----------------------------------------------------------
        # 🕵️‍♂️ 【现场案发现场收集区】
        # -----------------------------------------------------------
        node_id = item.nodeid  # 当前用例的唯一标识节点名
        exc_info = call.excinfo  # 捕获到的活体异常对象

        log.error(f"💥 拦截到用例执行失败！节点: {node_id}")

        # 将失败堆栈信息死死钉在 Allure 报告头部
        allure.attach(
            body=str(exc_info.longrepr),
            name="💥 案发现场完整 Traceback 报错堆栈",
            attachment_type=allure.attachment_type.TEXT
        )
