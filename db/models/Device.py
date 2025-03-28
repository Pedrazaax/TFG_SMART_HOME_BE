'''
Device model
'''

from typing import List, Union, Optional
from pydantic import BaseModel
from db.models.room import Room

class Command(BaseModel):
    '''comandos de los dispositivos'''
    code: str
    value: Union[str, int, bool]

class Device(BaseModel):
    '''Modelo de dispositivo'''
    id: Optional[str]
    name: Optional[str]
    id_device: str
    tipoDevice: str
    key: Optional[str] = None
    commands: Optional[List[Command]] = None
    create_time:Optional[str]
    update_time:Optional[str]
    ip:Optional[str]
    online:Optional[bool]
    model:Optional[str]
    room:Optional[Room]
