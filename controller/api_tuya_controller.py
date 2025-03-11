'''
Nombre controlador: api_tuya_controller
Descripción: Controlador para gestionar las peticiones relacionadas con las API keys de Tuya
'''

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from controller.auth_users_controller import current_user
from db.models.keys_api import KeysAPI
from db.models.user import User
from service import api_tuya_service

app = APIRouter(prefix="/keysAPI",
                    tags=["keysAPI"],
                    responses={status.HTTP_404_NOT_FOUND: {"detail":"No encontrado"}})

@app.get("/", response_model=Optional[KeysAPI])
async def keys_api(
    user: User = Depends(current_user)
):
    '''Obtener las keys de la API de Tuya'''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    return await api_tuya_service.get_keysAPI(user.username)

@app.post("/addKeys", response_model=KeysAPI)
async def add_keys(
    keys: KeysAPI = Body(...),
    authorization: str = Header(None),
    user: User = Depends(current_user)
):
    '''
    Guardar las keys de la API de Tuya
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    try:
        print("Autorización: ", authorization)
        return await api_tuya_service.registerKeys(keys)
    except Exception as e:
        print("Error al guardar las API keys (Controller): ", str(e))
        raise HTTPException(
            status_code=404,
            detail="No se han podido guardar las keys de la API"
            ) from e
    