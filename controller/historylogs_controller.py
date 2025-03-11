'''
Nombre controlador: historylogs_controller
Descripción: Controlador para obtener los logs y el historial de Home Assistant
'''

from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_users_controller import current_user
from db.models.user import User
from service import historylogs_service

app = APIRouter(prefix="/historylogs",
                    tags=["HistoryLogs"],
                        responses={404: {"detail":"Not found"}})

# Endpoint para obtener los logs de HA (Home Assistant)
@app.get("/getLogbook/{startTime}&{endTime}")
async def get_logs(start_time: str, end_time:str, user: User = Depends(current_user)):
    '''Obtiene los logs de Home Assistant en un periodo específico'''
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
        logs = await historylogs_service.get_logs_from_ha(token, dominio, start_time, end_time)
        print("Logs obtenidos: *********************************", logs)
        return logs
    except Exception as e:
        print("Error al obtener logs: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Endpoint para obtener el historial de HA en un periodo específico
@app.get("/getPeriod/{startTime}&{endTime}&{entity_id}")
async def get_history(
    start_time: str,
    end_time:str,
    entity_id:str,
    user: User = Depends(current_user)
    ):
    '''Obtiene el historial de Home Assistant en un periodo específico'''
    # Verificar si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Obtención del token y dominio de la base de datos
    token = user.homeAssistant.tokenHA
    dominio = user.homeAssistant.dominio
    print("Entity_id: ", entity_id)

    # Verifica si el token está vacío
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token no encontrado")
        # Verifica si el dominio está vacío
    if not dominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")
    try:
        history = await historylogs_service.get_history_from_ha(
            token,
            dominio,
            start_time,
            end_time
            )
        return history
    except Exception as e:
        print("Error al obtener historial: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)) from e
