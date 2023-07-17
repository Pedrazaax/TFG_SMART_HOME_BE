### Device model ###

from pydantic import BaseModel
from typing import List, Union, Optional

class Command(BaseModel):
    code: str
    value: Union[str, int, bool]

class Device(BaseModel):
    id: Optional[str]
    name: Optional[str]
    idDevice: str
    tipoDevice: str
    key: Optional[str] = None
    commands: Optional[List[Command]] = None
    create_time:Optional[str]
    update_time:Optional[str]
    ip:Optional[str]
    online:Optional[bool]
    model:Optional[str]