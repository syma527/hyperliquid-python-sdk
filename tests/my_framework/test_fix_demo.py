import pytest
import allure
import json
from tests.my_framework.tools.handle_logs import create_logger

log = create_logger("XSHOP")
# 模拟的测试数据弹药库
test_case_data = [
    {"user_id": 8001, "amount": 500, "title": "正常用户充值500元"}
]

class TestRecharge:

    @pytest.mark.parametrize('case_data', test_case_data)
    def test_user_recharge(self, case_data):
        # 🎯 测开规范 1：套上 DDT 后，第一时间动态更新报告用例标题
        allure.dynamic.title(f"充值测试 - {case_data['title']}")

        # 🎯 测开规范 2：步骤一 独立盒子
        with allure.step("步骤一：查询初始余额"):
            log.info(f"发送请求前，查询用户【{case_data['user_id']}】初始余额")
            initial_balance = 1000  # 模拟查询到的余额
            log.info(f"查询成功，当前初始余额为: {initial_balance}")

        # 🎯 测开规范 3：步骤二 独立盒子
        with allure.step("步骤二：发起充值请求"):
            # 从 case_data 动态提取入参，避免硬编码
            payload = {
                "user_id": case_data["user_id"],
                "amount": case_data["amount"]
            }
            log.info(f"🚀 撞击充值网关 ➡️ 入参: {payload}")

            mock_num = {
                "code": 200,
                "msg": "充值成功"
            }

            # 精准挂载在步骤二的肚子里
            allure.attach(
                json.dumps(payload, indent=4),
                name="充值请求 Payload JSON",
                attachment_type=allure.attachment_type.JSON
            )

            # 校验与日志捕获
            try:
                assert mock_num["code"] == 200, "接口状态码不符合预期，充值失败！"
                log.info(f"🎉 充值成功，成功充值 {payload['amount']} 元！")
            except AssertionError as e:
                log.error(f"❌ 充值断言失败！实际回执: {mock_num}")
                raise e