### User model ###

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str]
    username: str
    disabled: bool
    email: str
    password: str
    pwd2: str
