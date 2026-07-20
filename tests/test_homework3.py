# tests/test_user_management.py
import pytest
from tests.tools.handle_logs01 import my_log


@pytest.fixture(scope="class")
def class_logger():
    """类级别的 Logger，整个测试类共享"""
    return my_log("USER_MGMT")


class TestUserManagement:
    """用户管理模块测试"""

    def test_create_user(self, class_logger):
        class_logger.info("📝 测试创建用户")

        user_data = {
            "username": "alice",
            "email": "alice@example.com",
            "age": 25
        }

        class_logger.info(f"用户数据: {user_data}")
        class_logger.debug(f"用户名长度: {len(user_data['username'])}")

        # 实际测试逻辑
        assert user_data["age"] > 18
        class_logger.info("✅ 用户创建验证通过")

    def test_delete_user(self, class_logger):
        class_logger.info("🗑️ 测试删除用户")

        user_id = 12345
        class_logger.info(f"准备删除用户 ID: {user_id}")

        # 实际测试逻辑
        assert user_id > 0
        class_logger.info("✅ 用户删除验证通过")

    def test_update_user(self, class_logger):
        class_logger.info("✏️ 测试更新用户")

        update_fields = {"email": "new_email@example.com"}
        class_logger.info(f"更新字段: {update_fields}")

        # 实际测试逻辑
        assert "email" in update_fields
        class_logger.info("✅ 用户更新验证通过")
