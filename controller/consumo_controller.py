'''
Nombre controlador: consumo_controller
Descripción: Controlador de las pruebas de consumo
'''

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_users_controller import current_user
from db.models.user import User
from db.models.prueba_consumo import PruebaConsumo, TipoPrueba
from db.schemas.prueba_consumo import pruebas_consumo_schema, tipo_pruebas_schema
from db.client import client
from service import consumo_service

app = APIRouter(prefix="/consumo",
                    tags=["Consumo"],
                    responses={404: {"detail": "No encontrado"}})


@app.get("/", response_model=List[PruebaConsumo])
async def pruebas_consumo(user: User = Depends(current_user)):
    '''Devuelve la lista de pruebas de consumo'''
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    pruebas_consumo_list = pruebas_consumo_schema(client.PruebasConsumo.find())
    if len(pruebas_consumo_list) == 0:
        raise HTTPException(status_code=204, detail="La lista está vacía")

    return pruebas_consumo_list

@app.get("/getPruebas", response_model=List[TipoPrueba])
async def get_tipo_prubas(user: User = Depends(current_user)):
    '''
    Devuelve la lista de los tipos de pruebas
    '''
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )   
    tipo_pruebas = tipo_pruebas_schema(client.TipoPrueba.find())
    if len(tipo_pruebas) == 0:
        raise HTTPException(status_code=204, detail="La lista está vacía")

    return tipo_pruebas

@app.post("/create", response_model=PruebaConsumo, status_code=status.HTTP_201_CREATED)
async def create_pconsumo(p_consumo: PruebaConsumo, user: User = Depends(current_user)):
    '''
    Crea una nueva prueba de consumo
    '''
    try:
        # Verifica si el usuario está autenticado a través del token JWT en la cabecera
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
                )
        new_pconsumo = await consumo_service.create_pconsumo(p_consumo)
        return PruebaConsumo(**new_pconsumo)
    except Exception as e:
        print("Error (consumoController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

@app.post("/createTipoPrueba", response_model=TipoPrueba, status_code=status.HTTP_201_CREATED)
async def create_tipo_prueba(t_prueba:TipoPrueba, user: User = Depends(current_user)):
    '''
    Crea un nuevo tipo de prueba
    '''
    try:
        # Verifica si el usuario está autenticado a través del token JWT en la cabecera
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
                )
        new_tprueba = await consumo_service.create_tipo_prueba(t_prueba)
        return TipoPrueba(**new_tprueba)
    except Exception as e:
        print("Error (consumoController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

@app.delete(("/deleteTipoPrueba/{id}"),status_code=status.HTTP_204_NO_CONTENT)
async def delete_pconsumo(_id: str, user: User = Depends(current_user)):
    '''
    Elimina tipo de prueba
    '''
    try:
        # Verifica si el usuario está autenticado a través del token JWT en la cabecera
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autenticado"
                )
        await consumo_service.delete_pconsumo(_id)
        return {"message": "Prueba de consumo eliminada"}
    except Exception as e:
        print("Error (consumoController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e


@app.get("/getDispositivosSimulador")
async def get_dispositivos_simulador(user: User = Depends(current_user)):
    '''
    Listar Pruebas de Consumo de Dispositivos Simulador
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    try:
        return await consumo_service.get_dispositivos_simulador(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e
    