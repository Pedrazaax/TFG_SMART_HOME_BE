### Room model ###

from pydantic import BaseModel
from typing import Optional

class Room(BaseModel):
    id: Optional[str]
    name: str