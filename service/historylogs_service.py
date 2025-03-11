### Clase Service de HistoryLogs ###

import httpx

# Función para obtener logs de Home Assistant
async def get_logs_from_ha(token: str, dominio: str, startTime: str, endTime: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Cadena time con startTime y endTime
    time = f"{startTime}?end_time={endTime}"
    print("Time: ", time)

    url = f"{dominio}/api/logbook/{time}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

# Función para obtener historial de Home Assistant
async def get_history_from_ha(token: str, dominio: str, startTime: str, endTime: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Cadena time con startTime y endTime
    time = f"{startTime}?end_time={endTime}"
    print("Time: ", time)

    url = f"{dominio}/api/history/period/{time}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()