### User model ###

from pydantic import BaseModel
from typing import Optional , Tuple

class HomeAssistant(BaseModel):
    tokenHA: str
    dominio: str

class User(BaseModel):
    id: Optional[str]
    username: str
    disabled: bool
    email: str
    password: str
    pwd2: str
    homeAssistant: Optional[HomeAssistant]