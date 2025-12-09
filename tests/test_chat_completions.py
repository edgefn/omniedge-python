import os.path
import sys
import pytest
import asyncio


from omniedge import OmniEdge



class TestChatCompletions:

    @pytest.fixture
    def client(self):
        api_key  = os.getenv("OMNIEDGE_API_KEY")
        base_url  = os.getenv("BASE_URL")

        if not api_key:
            pytest.skip("OMNIEDGE_API_KEY not set")  # 或 raise pytest.UsageError
        if not base_url:
            pytest.skip("BASE_URL not set")

        client = OmniEdge(
            base_url=base_url ,
            api_key=api_key,
        )
        return client

    def test_api_key_base_url(self,client):
        expected_api_key = os.getenv("OMNIEDGE_API_KEY")
        assert client.sdk_configuration.security.api_key == expected_api_key, "API key mismatch"

    def test_client_initialization(self, client):
        """测试客户端初始化是否正常"""
        assert client is not None
        assert hasattr(client, 'chat')
        assert client.sdk_configuration is not None

    def test_basic_chat_completion(self, client):
        """测试基本的非流式聊天完成功能"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "你是谁"}
                ]
            )

            # 验证响应结构
            assert completion is not None,"completion mismatch"
            assert completion.result.choices is not None
            assert len(completion.result.choices) > 0
            assert completion.result.choices[0].message is not None
            assert completion.result.choices[0].message.content is not None
            assert len(completion.result.choices[0].message.content) > 0

            # 验证响应包含预期字段
            assert completion.result.id is not None
            assert completion.result.model is not None
            assert completion.result.created is not None

            print(f"Response content: {completion.result.choices[0].message.content}")

        except Exception as e:
            pytest.fail(f"Chat completion failed: {str(e)}")

    @pytest.mark.asyncio
    async def test_async_chat_completion(self, client):
        """测试异步聊天完成功能"""
        try:
            completion = await client.chat.create_async(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "你好，请介绍一下你自己"}
                ]
            )

            # 验证响应结构
            assert completion is not None
            assert completion.result.choices is not None
            assert len(completion.result.choices) > 0
            assert completion.result.choices[0].message is not None
            assert completion.result.choices[0].message.content is not None
            assert len(completion.result.choices[0].message.content) > 0

            print(f"Async response content: {completion.result.choices[0].message.content}")

        except Exception as e:
            pytest.fail(f"Async chat completion failed: {str(e)}")

    def test_chat_with_system_message(self, client):
        """测试包含系统消息的聊天"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "system", "content": "你是一个有用的AI助手"},
                    {"role": "user", "content": "今天天气怎么样"}
                ]
            )

            assert completion is not None
            assert completion.result.choices is not None
            assert len(completion.result.choices) > 0
            assert completion.result.choices[0].message.content is not None

            print(f"System message response: {completion.result.choices[0].message.content}")

        except Exception as e:
            pytest.fail(f"Chat with system message failed: {str(e)}")

    def test_chat_with_temperature(self, client):
        """测试不同temperature参数的聊天"""
        try:
            # 测试高temperature（更随机）
            completion_high = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "讲一个简短的故事"}
                ],
                temperature=0.5
            )

            # 测试低temperature（更确定）
            completion_low = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "讲一个简短的故事"}
                ],
                temperature=0.1
            )

            assert completion_high is not None
            assert completion_low is not None
            assert completion_high.result.choices[0].message.content != completion_low.result.choices[0].message.content

            print(f"High temperature response: {completion_high.result.choices[0].message.content}")
            print(f"Low temperature response: {completion_low.result.choices[0].message.content}")

        except Exception as e:
            pytest.fail(f"Chat with temperature failed: {str(e)}")

    def test_chat_with_multiple_messages(self, client):
        """测试多轮对话"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "你好"},
                    {"role": "assistant", "content": "你好！有什么我可以帮你的吗？"},
                    {"role": "user", "content": "请介绍一下你自己"}
                ]
            )

            assert completion is not None
            assert completion.result.choices is not None
            assert len(completion.result.choices) > 0
            assert completion.result.choices[0].message.content is not None

            print(f"Multi-message response: {completion.result.choices[0].message.content}")

        except Exception as e:
            pytest.fail(f"Multi-message chat failed: {str(e)}")

    def test_chat_with_different_models(self, client):
        """测试不同模型的聊天（如果可用）"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",  # 使用当前可用模型
                messages=[
                    {"role": "user", "content": "测试消息"}
                ]
            )

            assert completion is not None
            assert completion.result.model == "kimi-k2-turbo-preview"

        except Exception as e:
            pytest.fail(f"Chat with different model failed: {str(e)}")

    def test_chat_error_handling(self, client):
        """测试错误处理"""
        try:
            # 测试无效参数
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[],  # 空消息列表
            )
            pytest.fail("Should have raised an error for empty messages")

        except Exception as e:
            # 应该抛出异常
            assert e is not None
            print(f"Expected error caught: {type(e).__name__}: {str(e)}")

    def test_chat_with_custom_headers(self, client):
        """测试自定义HTTP头"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "测试自定义头"}
                ],
                http_headers={"X-Custom-Header": "test-value"}
            )

            assert completion.result is not None
            assert completion.result.choices is not None

        except Exception as e:
            pytest.fail(f"Chat with custom headers failed: {str(e)}")

    def test_chat_response_format(self, client):
        """测试响应格式"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "说'Hello World'"}
                ]
            )

            # 验证响应字段类型
            assert isinstance(completion.result.id, str)
            assert isinstance(completion.result.created, int)
            assert isinstance(completion.result.model, str)
            assert isinstance(completion.result.choices, list)
            assert len(completion.result.choices) > 0

            choice = completion.result.choices[0]
            assert isinstance(choice.index, int)
            assert choice.message is not None
            assert isinstance(choice.message.content, str)
            assert isinstance(choice.message.role, str)

        except Exception as e:
            pytest.fail(f"Chat response format test failed: {str(e)}")

    def test_chat_with_timeout(self, client):
        """测试超时设置"""
        try:
            completion = client.chat.create(
                model="kimi-k2-turbo-preview",
                messages=[
                    {"role": "user", "content": "测试超时"}
                ],
                timeout_ms=30000  # 30秒超时
            )

            assert completion is not None
            assert completion.result.choices is not None

        except Exception as e:
            pytest.fail(f"Chat with timeout failed: {str(e)}")