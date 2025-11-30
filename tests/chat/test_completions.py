import pytest

from src.omniedge._client import Omniedge
from src.omniedge._constants import BASE_URL,OMNIEDGE_API_KEY


class TestChatCompletions:
    @pytest.fixture
    def client(self):
        client=Omniedge(
            base_url=BASE_URL,
            api_key=OMNIEDGE_API_KEY,
        )
        return client

    def test_chat(self,client):
            completions=client.chat.completions.create(
                model="Qwen/Qwen2.5-Coder-32B-Instruct",
                messages=[
                    {"role":"user","content":"你是谁"}
                ]
            )
            assert len(completions.choices[0].message.content)!=0,"对话测试错误"
            print(completions.choices[0].message.content)