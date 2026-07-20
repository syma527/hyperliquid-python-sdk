import pytest
from urllib3 import connection_from_url


#1. 用@pytest.fixture
# 核心秘诀:加上scope='class' ,告诉fixture只点火一次
@pytest.fixture(scope='class')
def db_connection():
    # ----这就是你的unittest setupclass
    print('\n 类前置 全局数据库连接成功')
    connection_pool = {'status':'connected','max_limit':20}

    yield connection_pool

    # 这就是你的unittest teardownclass
    print('\n 关闭全局数据库连接,释放所有线程池(整个测试类只执行一次)')

# 编写测试类 pytest 里不需要继承任何父类

class TestUserBusiness:
    # 怎么让整个类都用上类前置
    def test_add_user(self,db_connection):
        print(f"执行测试 正在读取类夹具状态:{db_connection['status']}")
        assert db_connection['status'] == 'connected'

    def test_delete_user(self,db_connection):
        print(f"依然使用刚才的连接,成功删除用户a")
        assert db_connection['max_limit'] == 20


