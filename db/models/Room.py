### KeysAPI model ###

from pydantic import BaseModel
from typing import Optional, List
from db.models.Device import Device

class Room(BaseModel):
    id: Optional[str]
    name: str
    devices: List[Device] = None