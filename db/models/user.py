'''
Modelo de usuario
Descripción: Modelo de usuario que se utiliza para la autenticación de los usuarios
'''

from typing import Optional
from pydantic import BaseModel

class HomeAssistant(BaseModel):
    '''
    Clase con token de Home Assistant y dominio
    '''
    tokenHA: str
    dominio: str

class User(BaseModel):
    '''
    Clase con los datos de usuario
    '''
    id: Optional[str]
    username: str
    disabled: bool
    email: str
    password: str
    pwd2: str
    homeAssistant: Optional[HomeAssistant]
    