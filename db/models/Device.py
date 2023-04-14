### Thermostat model ###

from pydantic import BaseModel
from typing import List, Union

class Command(BaseModel):
    code: str
    value: Union[str, int, bool]

class Device(BaseModel):
    idDevice: str
    key: str
    commands: List[Command]