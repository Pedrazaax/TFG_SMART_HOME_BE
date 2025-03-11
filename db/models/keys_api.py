'''### KeysAPI model ###'''

from typing import Optional
from pydantic import BaseModel

class KeysAPI(BaseModel):
    '''Modelo de la colección keysAPI'''
    id: Optional[str]
    username: str
    access_id: str
    access_key: str
    api_endpoint: str
    mq_endpoint: str
    