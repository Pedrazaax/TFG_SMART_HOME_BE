'''### Room model ###'''

from typing import Optional
from pydantic import BaseModel

class Room(BaseModel):
    '''Modelo de habitación'''
    id: Optional[str]
    name: str
    
