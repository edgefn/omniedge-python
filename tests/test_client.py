import pytest

from src.omniedge._client import Omniedge
from src.omniedge._constants import BASE_URL,OMNIEDGE_API_KEY


class TestClient:
    @pytest.fixture
    def client(self):
        client=Omniedge(
            base_url=BASE_URL,
            api_key=OMNIEDGE_API_KEY,
        )
        return client

    def test_request(self,client):
        body=client.request("get","www.baidu.com")
        print(body)
