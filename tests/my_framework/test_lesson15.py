from unittest.mock import Mock
import requests
from tests.my_framework.common.api_client import ApiClient
import pytest
from tests.my_framework.common.exceptions import NetworkError, HttpStatusError, InvalidJsonError
from tests.my_framework.common.infoapi import InfoApi
def test_post_mock_networkerror(monkeypatch):

    fake_post = Mock()

    client = ApiClient("http://example.invalid")

    fake_post.side_effect = requests.exceptions.ConnectTimeout("boom")

    monkeypatch.setattr(client.session,'post',fake_post)

    with pytest.raises(NetworkError) as ei:
        client.post("/info",{"type": "meta"})
    fake_post.assert_called_with(
        "http://example.invalid/info",
        json={"type":"meta"},
        timeout=(3,30),

    )
    assert isinstance(ei.value.cause,requests.exceptions.ConnectTimeout)
    assert ei.value.__cause__ is ei.value.cause


def fake_response(status_code,response_text):
    resp = requests.Response()
    resp.status_code = status_code
    resp._content = response_text.encode('utf-8')
    resp.encoding = 'utf-8'
    return resp

def test_mock_servererror(monkeypatch):

    fake_post = Mock()


    fake_post.return_value = fake_response(500,'....')
    client = ApiClient("https://example")
    monkeypatch.setattr(client.session,'post',fake_post)

    with   pytest.raises(HttpStatusError) as ei:
        InfoApi(client).meta()
    assert ei.value.status_code == 500

    fake_post.assert_called_once_with("https://example/info", json={"type": "meta"}, timeout=(3, 30))


def test_not_json_mock(monkeypatch):

    fake_post = Mock()

    fake_post.return_value = fake_response(200, "<html>not json</html>")
    client = ApiClient("https://example")
    monkeypatch.setattr(client.session, "post", fake_post)

    with pytest.raises(InvalidJsonError) as ei:
        InfoApi(client).meta()

    assert "html" in ei.value.text

    fake_post.assert_called_once_with("https://example/info", json={"type": "meta"}, timeout=(3, 30))
