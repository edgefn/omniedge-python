from ...resources.chat.completions import Completions
from ..._base_client import SyncAPIClient

class Chat:
    def __init__(self,client:SyncAPIClient):
        self.completions=Completions(client)