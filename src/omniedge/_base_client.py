import platform
import uuid

import httpx


from ._constants import SDK_NAME,SDK_VERSION,PY_VERSION
from ._exceptions import *


# 异常工厂方法，解析请求错误，返回自定义异常
def _parse_response_error(response: httpx.Response) -> APIStatusError:
    status=response.status_code
    try:
        body=response.json()
        # 尝试从常见的错误格式中提取 message
        # OpenAI 错误响应规范 {"error": {"message": "..."}}
        if isinstance(body,dict) and "error" in body:
            message=body["error"].get("message",f"Error {status}")
        else:
            message = f"Error {status}"
    except Exception:
        body=response.text
        message = f"Error {status}"
    if status == 400:
        return BadRequestError(message, response, body)
    if status == 401:
        return AuthenticationError(message, response, body)
    if status == 403:
        return PermissionDeniedError(message, response, body)
    if status == 404:
        return NotFoundError(message, response, body)
    if status == 422:
        return UnprocessableEntityError(message, response, body)
    if status == 429:
        return RateLimitError(message, response, body)
    if status >= 500:
        return InternalServerError(message, response, body)

    return APIStatusError(message, response, body)


def get_os_name() -> str:
    system = platform.system()
    if system == "Darwin":
        return "macOS"
    elif system == "Java":
        return "Jython"
    return system  # Linux, Windows, etc.

#同步客户端
class SyncAPIClient:
    def __init__(self,
                 *, api_key:str,
                 base_url:str,
                 timeout:float=60.0,
                 max_retries:int=2,
                 custom_headers:None|dict[str,str]=None):
        self.api_key=api_key
        self.max_retries=max_retries
        self.timeout=timeout
        self.headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"{SDK_NAME}/{SDK_VERSION} Python/{PY_VERSION}",
            f"X-{SDK_NAME}-Lang": "python",
            f"X-{SDK_NAME}-OS": get_os_name(),
        }
        if custom_headers is not None:
            self.headers.update(custom_headers)

        self._client=httpx.Client(base_url=base_url,
                                  headers=self.headers,
                                  timeout=self.timeout)

    def _build_request(self):
        pass

    def request(self,
                method:str,
                path:str,
                *,
                cast_to: any= None,  # 预留给未来做json数据类型转换
                options: dict[str, any]|None= None,#本次请求的自定义参数设置
                **kwargs,
                )->str|None:
        timeout=self.timeout
        headers=self.headers.copy()
        if options is not None:
            if "timeout" in options:
                timeout=options["timeout"]
            if "headers" in options:
                headers.update(options["headers"])
        test_request = httpx.Request(method="post", url="null")
        #TODO openai 使用build_client 构建request 这里先test，后面再跟进
        try:
            response=self._client.request(
                method=method,
                url=path,
                timeout=timeout,
                headers=headers,
                **kwargs,
            )

        except httpx.TimeoutException as err:
            raise APITimeoutError(request=test_request)
        except httpx.RequestError as err:
            raise APIConnectionError(request=test_request)

        #检查 HTTP 状态码
        if not (200 <= response.status_code < 300):
            raise  _parse_response_error(response)
        # 204 No Content
        if response.status_code==204:
            return None

        try:
            return response.json()
        except Exception:
            return response.text

    def post(self,path: str, **kwargs):
        return self.request("post", path, **kwargs)


    def get(self,path: str, **kwargs):
        return self.request("get", path, **kwargs)

    def delete(self,path: str, **kwargs):
        return self.request("delete", path, **kwargs)

    def close(self):
        self._client.close()


    def __enter__(self):
        return self


    def __exit__(self,exc_type, exc_value, traceback):
        self.close()



# # 异步客户端
# class AsyncAPIClient:
#     def __init__(self,
#                  *,
#                  base_url: str,
#                  api_key: str,
#                  timeout: float = 60.0,
#                  max_retries: int = 2,
#                  custom_header: None | Mapping[str, str] = None):
#         self.api_key = api_key
#         self.max_retries = max_retries
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#             "User-Agent": f"{SDK_NAME}/{SDK_VERSION} Python/{PY_VERSION}",
#             f"X-{SDK_NAME}-Lang": "python",
#             f"X-{SDK_NAME}-OS": get_os_name(),
#             "X-Request-ID": str(uuid.uuid4()),
#         }
#         if custom_header is not None:
#             headers.update(custom_header)
#
#         self._client = httpx.AsyncClient(base_url=base_url,
#                                     headers=headers,
#                                     timeout=timeout)
#
#     async def request(self,
#                 method: str,
#                 path: str,
#                 **kwargs,
#                 ) -> str | None:
#
#         try:
#             response = await self._client.request(
#                 method=method,
#                 url=path,
#                 **kwargs,
#             )
#
#         except httpx.TimeoutException as err:
#             raise APITimeoutError(message="连接超时")
#         except httpx.RequestError as err:
#             raise APIConnectionError(message="请求错误")
#
#         # 检查 HTTP 状态码
#         if 200 <= response.status_code < 300:
#             raise _parse_response_error(response)
#         # 204 No Content
#         if response.status_code == 204:
#             return None
#
#         try:
#             response.json()
#         except Exception:
#             return response.text
#
#     async def post(self, path: str, **kwargs):
#         return await self.request("post", path, **kwargs)
#
#     async def get(self, path: str, **kwargs):
#         return await self.request("get", path, **kwargs)
#
#     async def delete(self, path: str, **kwargs):
#         return await self.request("delete", path, **kwargs)
#
#     async def close(self):
#         await self._client.close()
#
#     async def __aenter__(self):
#         return self
#
#     async def __aexit__(self, exc_type, exc_value, traceback):
#         await self.close()
