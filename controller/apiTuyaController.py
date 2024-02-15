from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from controller.auth_usersController import current_user
from db.models.KeysAPI import KeysAPI
from db.models.user import User
from db.schemas.KeysAPI import keysAPI_schema
from db.client import client
from service import apiTuyaService

app = APIRouter(prefix="/keysAPI",
                    tags=["keysAPI"],
                    responses={status.HTTP_404_NOT_FOUND: {"detail":"No encontrado"}})

@app.get("/", response_model=Optional[KeysAPI])
async def keysAPI(
    user: User = Depends(current_user)
):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    return await apiTuyaService.get_keysAPI(user.username)

@app.post("/addKeys", response_model=KeysAPI)
async def addKeys(
    keys: KeysAPI = Body(...),
    authorization: str = Header(None),
    user: User = Depends(current_user)
):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")

    # Guardar las keys en la bbdd para utilizarlas en el usuario
    try:
        return await apiTuyaService.registerKeys(keys)
    except Exception as e:
        print("Error al guardar las API keys (Controller): ", str(e))
        raise HTTPException(status_code=404, detail="No se han podido guardar las keys de la API")