from __future__ import annotations

import httpx
from typing_extensions import Literal
from .types.chat import ChatCompletion

__all__=[
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError"
]


#错误基类
class OmniedgeError(Exception):
    pass

#模型回答外的业务错误基类
class APIError(OmniedgeError):
    message:str #错误摘要
    request:httpx.Request #原始请求头
    body:object|None #原始请求体
    code:str|None #业务错误代码
    param:str|None #具体错误参数
    type:str|None #错误分类 服务端错误或者客户端错误
    def __init__(self,message:str,
                 *,
                 request:httpx.Request,
                 body:object|None):
        self.message=message
        self.request=request
        self.body=body
        if isinstance(body,dict):
            error = body.get("error", {})
            self.code=error.get("code")
            self.param = error.get("param")
            self.type=error.get("type")
        else:
            self.code = None
            self.param = None
            self.type = None

#模型回答长度错误
class LengthFinishReasonError(OmniedgeError):
    completion: ChatCompletion
    def __init__(self, *, completion: ChatCompletion) -> None:
        msg = "Could not parse response content as the length limit was reached"
        if completion.usage:
            msg += f" - {completion.usage}"

        super().__init__(msg)
        self.completion = completion

#模型回答被模型过滤错误
class ContentFilterFinishReasonE(OmniedgeError):
    def __init__(self) -> None:
        super().__init__(
            f"Could not parse response content as the request was rejected by the content filter",
        )


#响应数据校验错误
class APIResponseValidationError(APIError):
    response: httpx.Response
    status_code: int
    def __init__(self, response: httpx.Response, body: object | None, *, message: str | None = None) -> None:
        super().__init__(message or "Data returned by API invalid for expected schema.", request=response.request, body=body)
        self.response = response
        self.status_code = response.status_code

#-------------------------------请求连接Error------------------------------

#连接错误
class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.", request: httpx.Request) -> None:
        super().__init__(message, request=request, body=None)

#连接超时错误
class APITimeoutError(APIConnectionError):
    def __init__(self, request: httpx.Request) -> None:
        super().__init__(message="Request timed out.", request=request)



#--------------------------------具体响应 4xx/5xx类Error------------------------------------

#具体响应 4xx/5xx类Error
class APIStatusError(APIError):
    response: httpx.Response
    status_code: int
    request_id: str | None
    def __init__(self, message: str, response: httpx.Response, body: object | None) -> None:
        super().__init__(message, request=response.request, body=body)
        self.response = response
        self.status_code = response.status_code
        self.request_id = response.headers.get("x-request-id")


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401


class PermissionDeniedError(APIStatusError):
    status_code: Literal[403] = 403


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422


class RateLimitError(APIStatusError):
    status_code: Literal[429] = 429


class InternalServerError(APIStatusError):
    pass