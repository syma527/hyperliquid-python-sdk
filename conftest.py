# tests/conftest.py 文件的完全体
import pytest
from tests.common.api_client import ApiClient
from pathlib import Path
# import sys
# tests_dir = Path(__file__).parent / 'tests'
# if str(tests_dir) not in sys.path:
#     sys.path.insert(0,str(tests_dir))
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