from typing import Literal

from pydantic import  BaseModel


class ChatCompletionMessage(BaseModel):
    role: Literal["assistant"] #消息角色
    content:str|None #消息内容



class Choice(BaseModel):
    index :int #第几条回答
    message :ChatCompletionMessage #回答消息
    #结束回答原因，"stop" (正常结束), "length" (超长截断), "content_filter" (被过滤)
    finish_reason:  Literal["stop", "length", "content_filter", ]

class CompletionUsage(BaseModel):
    prompt_tokens:int #提问token
    completion_tokens:int #回答消耗
    total_tokens: int  # 总消耗


class ChatCompletion(BaseModel):
    id :str  #唯一请求 ID
    object:Literal["chat.completion"]="chat.completion" # 功能类型表示
    created: int  # 创建时间
    model:str #模型名称
    choices:list[Choice] #回答列表

    usage: CompletionUsage|None=None


