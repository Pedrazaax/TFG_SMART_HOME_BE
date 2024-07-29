#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_usersController import current_user
from db.models.user import User
from service import localDeviceService

app = APIRouter(prefix="/localMeasures",
                     tags=["Local Measures"],
                     responses={404: {"detail":"Not found"}})

@app.put("/updateMeasurementsConsumption")
async def get_pconsumo(user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")

    # Crear un conjunto para rastrear los valores ya vistos
    dispositivos_vistos = set()
    # Crear una lista para los objetos únicos
    dispositivos = []

    try:
        pconsumos = await localDeviceService.get_pconsumo(user)
        for pconsumo in pconsumos:
            if pconsumo['device'] not in dispositivos_vistos:
                dispositivos.append({
                    "device":pconsumo['device'],
                    "estado":"",
                    "consumoMedio":0,
                    "potenciaMedia":0,
                    "intensidadMedia":0,
                    "etiqueta":""
                })
                dispositivos_vistos.add(pconsumo['device'])
        return dispositivos
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))