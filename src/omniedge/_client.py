import os
from functools import cached_property

import httpx

from ._constants import OMNIEDGE_API_KEY,BASE_URL
from ._base_client import SyncAPIClient
from .resources.chat import Chat

# print("package",__package__)

class Omniedge(SyncAPIClient):
    api_key: str
    organization: str | None
    project: str | None
    webhook_secret: str | None

    websocket_base_url: str | httpx.URL | None
    """Base URL for WebSocket connections.

    If not specified, the default base URL will be used, with 'wss://' replacing the
    'http://' or 'https://' scheme. For example: 'http://example.com' becomes
    'wss://example.com'
    """

    def __init__(self,
                 *, api_key: str|None,
                 base_url: str|None,
                 timeout: float = 60.0,
                 max_retries: int = 2,
                 custom_headers: None | dict[str, str] = None):

        if api_key is None:
            #尝试读取环境变量
            api_key=os.environ.get(OMNIEDGE_API_KEY)

        if api_key is None:
            raise ValueError(
                f"The api_key client option must be set either by passing api_key to the client or by setting the {OMNIEDGE_API_KEY} environment variable")
        if base_url is None:
            base_url=BASE_URL

        super().__init__(base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=custom_headers,)

        # self.chat=Chat(self)

    @cached_property
    def chat(self) -> Chat:
        from .resources.chat import Chat

        return Chat(self)