### KeysAPI model ###

from pydantic import BaseModel
from typing import Optional

class KeysAPI(BaseModel):
    id: Optional[str]
    username: str
    access_id: str
    access_key: str
    api_endpoint: str
    mq_endpoint: str