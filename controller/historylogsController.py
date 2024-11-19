#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_usersController import current_user
from db.models.user import User
from service import historylogsService

app = APIRouter(prefix="/historylogs", 
                    tags=["HistoryLogs"],
                        responses={404: {"detail":"Not found"}})

# Endpoint para obtener los logs de HA (Home Assistant)
@app.get("/getLogbook/{startTime}&{endTime}")
async def get_logs(startTime: str, endTime:str, user: User = Depends(current_user)):

    # Verificar si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    # Obtención del token y dominio de la base de datos
    token = user.homeAssistant.tokenHA
    dominio = user.homeAssistant.dominio

    # Verifica si el token está vacío
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token no encontrado")
    
    # Verifica si el dominio está vacío
    if not dominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")

    try:
        logs = await historylogsService.get_logs_from_ha(token, dominio, startTime, endTime)
        print("Logs obtenidos: *********************************", logs)
        return logs
    except Exception as e:
        print("Error al obtener logs: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Endpoint para obtener el historial de HA en un periodo específico
@app.get("/getPeriod/{startTime}&{endTime}&{entity_id}")
async def get_history(startTime: str, endTime:str, entity_id:str, user: User = Depends(current_user)):

    # Verificar si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Obtención del token y dominio de la base de datos
    token = user.homeAssistant.tokenHA
    dominio = user.homeAssistant.dominio

    # Verifica si el token está vacío
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token no encontrado")
    
    # Verifica si el dominio está vacío
    if not dominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")

    try:
        history = await historylogsService.get_history_from_ha(token, dominio, startTime, endTime, entity_id)
        return history
    except Exception as e:
        print("Error al obtener historial: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
