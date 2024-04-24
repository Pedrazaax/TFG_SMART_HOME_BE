#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_usersController import current_user
from typing import List
from db.models.user import User
from service import localDeviceService

app = APIRouter(prefix="/localDevices",
                     tags=["Local Devices"],
                     responses={404: {"detail":"Not found"}})

# Guardar token de autenticación y dominio proveniente del cliente
@app.post("/saveHA")
async def save_token(token: str, dominio: str, user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    # Comprueba que el token no esté vacio
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token vacío")
    
    # Comprueba que el token sea válido
    if len(token) < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")
    
    # Comprueba que el dominio no esté vacio
    if not dominio:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dominio vacío")
    
    # Comprueba que el dominio sea válido
    if not localDeviceService.validate_domain(dominio):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dominio inválido")

    try:
        await localDeviceService.save_homeAssistant(token, dominio, user)
        print("Token guardado correctamente")
        print("Token: ", token)
        return user.tokenHA
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Listar tipo de pruebas / scripts
@app.get("/listScripts")
async def list_scripts(user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    # Obtención del token de la base de datos
    token = user.homeAssistant[0].tokenHA

    # Obtención del dominio de la base de datos
    dominio = user.homeAssistant[0].dominio

    # Verifica si el token está vacío
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token no encontrado")
    
    # Verifica si el dominio está vacío
    if not dominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")
    
    try:
        scripts = await localDeviceService.list_scripts(token, dominio)
        print("Lista de scripts")
        print("Scripts: ", scripts)
        return scripts
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Lista local devices Home Assistant
@app.get("/")
async def local_devices(user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    # Trae el token de la base de datos
    token = user.tokenHA

    # Verifica si el token está vacío
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token no encontrado")
    
    try:
        print("Lista de dispositivos locales")
        print("Dispositivos: ", user.local_devices)
        # Devuelve la lista de local devices
        return user.local_devices
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))