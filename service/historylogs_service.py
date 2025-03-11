'''
### Clase Service de HistoryLogs ###
Descripción: Clase que contiene las funciones para obtener logs e historial de Home Assistant 
'''

import httpx

async def get_logs_from_ha(token: str, dominio: str, start_time: str, end_time: str):
    '''
    Función para obtener logs de Home Assistant
    '''
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Cadena time con startTime y endTime
    time = f"{start_time}?end_time={end_time}"
    print("Time: ", time)

    url = f"{dominio}/api/logbook/{time}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

async def get_history_from_ha(token: str, dominio: str, start_time: str, end_time: str):
    '''
    Función para obtener historial de Home Assistant
    '''
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Cadena time con startTime y endTime
    time = f"{start_time}?end_time={end_time}"
    print("Time: ", time)

    url = f"{dominio}/api/history/period/{time}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    