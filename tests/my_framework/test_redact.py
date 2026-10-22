from tests.my_framework.tools.redact import mask_secret, redact_text


def test_longkey_mask():
    """超过8位数据加掩码"""
    fake = "0x" + "a" * 64
    assert mask_secret(fake) == "0xaa***aaaa"


def test_short_mask():
    """低于8位数据加掩码"""
    short_fake = mask_secret("12345678")
    assert short_fake == "***", f"assert failed,actually return {short_fake}"


def test_redact_text():
    """文本中含有秘钥信息查找加掩码"""
    original_text = "key=0x" + "a" * 64 + "结束"
    res_redact = redact_text(original_text)

    assert res_redact == "key=0xaa***aaaa结束", f"don't have this sentence{res_redact}"


def test_normal_text():
    """普通信息原样返回"""
    res_normal = redact_text("hello world")
    assert res_normal == "hello world", f"failed,actually return is {res_normal}"


def test_empty_string():
    """空字符串原样返回"""
    res_empty = mask_secret("")
    assert res_empty == "", f"failed,actually return is {res_empty}"
