from unittest.mock import Mock
import requests
from tests.my_framework.common.api_client import ApiClient
import pytest
from tests.my_framework.common.exceptions import NetworkError
def test_post_mock_networkerror(monkeypatch):

    fake_post = Mock()

    client = ApiClient("http://example.invalid")

    fake_post.side_effect = requests.exceptions.ConnectTimeout("boom")

    monkeypatch.setattr(client.session,'post',fake_post)

    with pytest.raises(NetworkError) as ei:
        client.post("/info",{"type": "meta"})
    fake_post.assert_called_once()
    assert isinstance(ei.value.cause,requests.exceptions.ConnectTimeout)
