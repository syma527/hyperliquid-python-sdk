import re


def mask_secret(text: str) -> str:
    """加掩码"""
    if not text:
        return ""
    if len(text) <= 8:
        return "***"
    return text[:4] + "***" + text[-4:]


def redact_text(text: str) -> str:
    """长文本里面查找秘钥信息加掩码,其他信息原样返回"""
    return re.sub(r"0[xX][0-9a-fA-F]{64}", lambda x: mask_secret(x.group(0)), text)


if __name__ == "__main__":
    res = mask_secret("155595245")
    print(res)
