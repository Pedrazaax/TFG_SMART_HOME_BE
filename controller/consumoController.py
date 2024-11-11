### Clase Controller de consumo ###

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_usersController import current_user
from db.models.user import User
from db.models.PruebaConsumo import PruebaConsumo, TipoPrueba
from db.schemas.pruebaConsumo import pruebasConsumo_schema, tipoPruebas_schema
from db.client import client
from service import consumoService

app = APIRouter(prefix="/consumo",
                    tags=["Consumo"],
                    responses={404: {"detail": "No encontrado"}})


@app.get("/", response_model=List[PruebaConsumo])
async def pruebasConsumo(user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    pruebasConsumo = pruebasConsumo_schema(client.PruebasConsumo.find())
    if len(pruebasConsumo) == 0:
         raise HTTPException(status_code=204, detail="La lista está vacía")

    return pruebasConsumo

@app.get("/getPruebas", response_model=List[TipoPrueba])
async def getTipoPrubas(user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    tipoPruebas = tipoPruebas_schema(client.TipoPrueba.find())
    if len(tipoPruebas) == 0:
         raise HTTPException(status_code=204, detail="La lista está vacía")

    return tipoPruebas

# Hacer una prueba de consumo
@app.post("/create", response_model=PruebaConsumo, status_code=status.HTTP_201_CREATED)
async def createPConsumo(pConsumo: PruebaConsumo, user: User = Depends(current_user)):

    try:
        # Verifica si el usuario está autenticado a través del token JWT en la cabecera
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
        new_pConsumo = await consumoService.createPConsumo(pConsumo)
        return PruebaConsumo(**new_pConsumo)
    except Exception as e:
        print("Error (consumoController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Crear un nuevo tipo de prueba
@app.post("/createTipoPrueba", response_model=TipoPrueba, status_code=status.HTTP_201_CREATED)
async def createTipoPrueba(tPrueba:TipoPrueba, user: User = Depends(current_user)):
    try:
        # Verifica si el usuario está autenticado a través del token JWT en la cabecera
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
        new_tPrueba = await consumoService.createTipoPrueba(tPrueba)
        return TipoPrueba(**new_tPrueba)
    except Exception as e:
        print("Error (consumoController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Eliminar tipo de prueba
@app.delete(("/deleteTipoPrueba/{id}"),status_code=status.HTTP_204_NO_CONTENT)
async def deletePConsumo(id: str, user: User = Depends(current_user)):

    try:
        # Verifica si el usuario está autenticado a través del token JWT en la cabecera
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")

        await consumoService.deletePConsumo(id)
        return {"message": "Prueba de consumo eliminada"}
        
    except Exception as e:
        print("Error (consumoController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Listar Pruebas de Consumo
@app.get("/getDispositivosSimulador")
async def get_dispositivosSimulador(user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    try:
        return await consumoService.get_dispositivosSimulador(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))