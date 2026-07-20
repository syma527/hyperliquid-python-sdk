import pytest
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
# 注意：底层的账户加签通常需要用到本地的本地钱包账户类，我们从 eth_account 导入它来当真正的参数
from eth_account import Account


def test_invalid_secret_key_should_fail():
    # 1. 故意构造一个非法的、错误的私钥字符串（注入故障）
    fake_secret_key = "0xthis_is_a_wrong_and_invalid_secret_key_12345"

    # 2. 核心测开黑客思维：我们预期下面这行代码【绝对会引发 ValueError 崩溃】
    with pytest.raises(ValueError) as exc_info:
        # 💡 【核心重构在这里】：
        # 真实的 SDK 中，Exchange 不需要直接传私钥字符串，而是需要一个用私钥初始化好的 Account 对象！
        # 我们在这里故意用假私钥去生成本地账户，看看底层的 eth-account 零件会不会直接爆炸
        local_account = Account.from_key(fake_secret_key)

        # 如果上面没爆炸（概率极低），我们再把它塞给 Exchange 看看它在对齐名字的情况下怎么死：
        exchange = Exchange(
            wallet=local_account,
            base_url=constants.MAINNET_API_URL
        )

    # 3. 盾牌拦截成功，提取出底层抛出的真实报错文字
    error_msg = str(exc_info.value)
    print(f"\n【异常测试成功】框架成功捕获到预期的系统报错信息: {error_msg}")

    # 4. 断言：校验底层的报错提示是否足够专业
    assert "non-hexadecimal" in error_msg or "invalid" in error_msg.lower() or "hex" in error_msg.lower()