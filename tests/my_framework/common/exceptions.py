class ApiError(Exception):
    pass


class NetworkError(ApiError):
    """网络异常,返回错误信息"""
    def __init__(self, message: str, cause: Exception) -> None:
        super().__init__(message)
        self.cause = cause


class HttpStatusError(ApiError):
    """HTTP 状态码不符合预期；携带状态码与响应体片段"""

    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(f"unexpected status {status_code}: {body[:200]}")


class InvalidJsonError(ApiError):
    """无效json解码失败,返回响应"""
    def __init__(self, text: str) -> None:
        self.text = text[:200]
        super().__init__(f"invalid JSON response: {self.text}")
