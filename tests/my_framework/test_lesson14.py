

import pytest
import requests
from tests.my_framework.common.assert_common import assert_status
from tests.my_framework.common.exceptions import HttpStatusError,InvalidJsonError,NetworkError
from tests.my_framework.common.infoapi import InfoApi
from tests.my_framework.common.api_client import ApiClient

def make_response(status_code: int,response_text) -> requests.Response:
    resp = requests.Response()
    resp.status_code = status_code
    resp._content=response_text.encode("utf-8")
    resp.encoding = "utf-8"
    return resp




def test_assert_status_raise_http_status_error():
    resp = make_response(500,f"server is bad")
    with pytest.raises(HttpStatusError) as e:
        assert_status(resp,200)

    assert e.value.status_code == 500





class FakeClient:
    """假的 ApiClient：post 直接返回一个固定响应"""
    def post(self, endpoint, json_data=None):
        return make_response(200, "<html>not json</html>")


def test_query_raises_invalid_json_error():
    """响应不是 JSON 时，_query 应包装成 InvalidJsonError"""
    api = InfoApi(FakeClient())

    with pytest.raises(InvalidJsonError) as ei:
        api.meta()

    assert "html" in ei.value.text

class FakeSession:
    """假的 requests.Session：一调用就抛超时"""
    def post(self, *args, **kwargs):
        raise requests.exceptions.ConnectTimeout("boom")


def test_client_wraps_timeout_as_network_error():
    """传输层异常必须包装成 NetworkError，并保留原始异常"""
    client = ApiClient("http://example.invalid")
    client.session = FakeSession()          # 构造完再换掉，避开 headers 初始化

    with pytest.raises(NetworkError) as ei:
        client.post("/info", {"type": "meta"})

    assert isinstance(ei.value.cause, requests.exceptions.ConnectTimeout)