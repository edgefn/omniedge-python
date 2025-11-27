

from ..._base_client import SyncAPIClient

from ...types.chat.chat_completion import ChatCompletion



class Completions:
    def __init__(self,client:SyncAPIClient):
        self._client=client

    def create(self,
               *,
               model:str,
               messages:list[dict[str,str]],
               temperature:float|None=1.0,
               **kwargs,)->ChatCompletion:
        payload={
            "model":model,
            "messages":messages,
            "temperature":temperature,
            **kwargs,
        }
        response_dict=self._client.post(path="/chat/completions",
                                        json=payload)

        if response_dict is None:
            raise ValueError("API return empty response")

        return ChatCompletion.model_validate(response_dict)
