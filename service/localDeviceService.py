### Clase Service de dispositivos locales ###

from db.models.user import User
from db.models.PruebaConsumo import TipoPruebaLocal, PruebaConsumoLocal
from db.schemas.pruebaConsumo import tiposPruebaLocal_schema, pruebasConsumoLocal_schema
from fastapi import HTTPException, status
from typing import List
from asyncio import sleep
import time
from datetime import datetime
from db.client import client
from bson import ObjectId
import httpx
import numpy as np

# URLs para las peticiones
CURRENT_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_current"
VOLTAGE_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_voltage"
ENERGY_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_energy"
POWER_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_power"

# Valores a restar
EB20_CURRENT = 0.09
EB20_ENERGY = 0.084
EB20_POWER = 14

async def save_homeAssistant(token: str, dominio: str, user: User):
    try:
        # Crear tupla homeAssistant
        homeAssistant = (token, dominio)

        # Comprueba si el usuario tiene ya token y dominio
        if user.homeAssistant is not None:
            # Elimina la tupla que tenga guardada
            user.homeAssistant.clear()
        else:
            # Guarda la nueva tupla guardando el token y dominio
            user.homeAssistant = homeAssistant
            client.users.update_one({"_id": ObjectId(user.id)}, {"$set": {"homeAssistant": user.homeAssistant}})

    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def validate_domain(dominio: str, user: User):
    try:
        # Declaración de flag de tipo booleano
        flag: bool = True

        # Comprueba que empiece por http:// o https://
        if not dominio.startswith("http://") and not dominio.startswith("https://"):
            print('Dominio', dominio)
            print("Dominio no empieza por http:// o https://")
            flag = False
            
        # Comprueba que después de http:// o https:// haya algún carácter, luego un punto y de nuevo caracter
        if not dominio[7:].split(".")[0] or not dominio[7:].split(".")[1]:
            print('Dominio', dominio)
            print("Dominio no tiene caracteres después de http:// o https://")
            flag = False

        # Si el dominio acaba en / se le quita y se guarda el nuevo dominio
        if dominio.endswith("/"):
            dominio = dominio[:-1]
            client.users.update_one({"_id": ObjectId(user.id)}, {"$set": {"homeAssistant.dominio": dominio}})

        return flag

    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def check_name(name: str, user: User, key: str):
    try:
        # Comprueba si el nombre ya existe en la base de datos
        if key == "pConsumo":
            if client.pruebaConsumoLocal.find_one({"userName": user.username, "name": name}):
                return True
            else:
                return False
        elif key == "tPrueba":
            if client.tipoPruebaLocal.find_one({"userName": user.username, "name": name}):
                return True
            else:
                return False
        else:
            raise ValueError("Invalid key")

    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
async def listAll(token: str, dominio: str):
    try:
        print("Listando scripts")
        
        # Inicialización de HTTP Headers con token bearer
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # URL de la petición GET
        url = f"{dominio}/api/states"

        # Petición GET a la API de Home Assistant
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
            responseJson = response.json()  # Parsea la respuesta JSON a un objeto Python
            return responseJson
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def save_tprueba(data: dict, user: User):
    try:
        print("Guardando tipo de prueba")

        # Obtiene los datos del JSON
        name = data.get('name')
        category = data.get('category')
        device = data.get('device')
        intervalos = data.get('intervalos')

        # Creación de objeto TipoPruebaLocal
        tipoPruebaLocal = TipoPruebaLocal(
            userName=user.username,
            name=name,
            category=category,
            device=device,
            intervalos=intervalos
        )

        # Guarda el objeto en la base de datos
        client.tipoPruebaLocal.insert_one(tipoPruebaLocal.dict())

        return tipoPruebaLocal
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def delete_tprueba(name: str, user: User):
    try:
        print("Borrando tipo de prueba")

        # Elimina el objeto de la base de datos
        client.tipoPruebaLocal.delete_one({"userName": user.username, "name": name})

        return {"message": "Tipo de prueba eliminado"}
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_pconsumo(name: str, user: User):
    try:
        print("Borrando prueba de consumo")

        # Elimina el objeto de la base de datos
        client.pruebaConsumoLocal.delete_one({"userName": user.username, "name": name})

        return {"message": "Prueba de consumo eliminada"}
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def get_tprueba(user: User):
    try:
        print("Listando tipos de prueba")

        # Obtiene los tipos de prueba de la base de datos del usuario
        tipoPruebaLocal = tiposPruebaLocal_schema(client.tipoPruebaLocal.find({"userName": user.username}))

        if len(tipoPruebaLocal) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay tipos de prueba guardados")

        return tipoPruebaLocal
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def get_pconsumo(user: User):
    try:
        print("Listando pruebas de consumo")

        # Obtiene las pruebas de consumo de la base de datos del usuario
        pruebaConsumoLocal = pruebasConsumoLocal_schema(client.pruebaConsumoLocal.find({"userName": user.username}))
    
        if len(pruebaConsumoLocal) == 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No hay pruebas de consumo guardadas")
        else:
            return pruebaConsumoLocal
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def save_pconsumo(data: dict, user: User):
    try:

        # Data:  {'name': 'a', 'category': 'light', 'device': 'light.smart_bulb_tuya_1', 'tipoPrueba': 'Prueba1', 'socket': 'switch.smart_plug_tuya_1'}

        print("Guardando prueba de consumo")

        # Inicialización de variables
        timeTotal = 0
        consumos = []
        consumoMediana = 0

        # Inicialización de HTTP Headers con token bearer
        headers = {
                "Authorization": f"Bearer {user.homeAssistant.tokenHA}",
                "Content-Type": "application/json"
            }

        # URL de la petición POST
        url = f"{user.homeAssistant.dominio}/api/services/script/turn_on"

        # Obtiene los datos del JSON
        name = data.get('name')
        category = data.get('category')
        device = data.get('device')
        tipoPrueba = data.get('tipoPrueba')
        enchufe = data.get('socket')

        # Obtiene el tipo de prueba de la base de datos
        tipoPrueba = client.tipoPruebaLocal.find_one({"userName": user.username, "name": tipoPrueba})

        print("Tipo de prueba: ", tipoPrueba)

        # Obtiene los intervalos del tipo de prueba
        intervalos = []
        for intervalo in tipoPrueba["intervalos"]:
            intervalos.append(intervalo)

        if enchufe == "switch.athom_smart_plug_v2_9d8b76_smart_plug_v2":
            # Inicializar la bombilla a estado EB20 para hacer prueba de consumo.
            async with httpx.AsyncClient() as cliente:
                body = {
                    "entity_id": "script.eb20"
                }
                response = await cliente.post(url, headers=headers, json=body)
                response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
        
        print("Esperando 10 segundos...")
        # Espera 10 segundos
        await sleep(10)

        # Recorremos la lista de intervalos del tipo de prueba
        for intervalo in intervalos:
            # Comprueba que el tiempo del intervalo sea mayor que 0
            if intervalo["time"] <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El tiempo del intervalo debe ser mayor que 0")
            
            # Calculamos el tiempo total de la prueba
            timeTotal += intervalo["time"]

            # Inicializamos el dispositivo con su estado
            async with httpx.AsyncClient() as cliente:
                body = {
                    "entity_id": intervalo["script"]
                }
                response = await cliente.post(url, headers=headers, json=body)
                response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
            
            # Calcular consumo del intervalo
            intervalo["consumo"], intervalo["current"], intervalo["voltage"], intervalo["energy"], intervalo["power"] = await calculate_average_consumption(intervalo["time"], headers, enchufe)

            # Lista de consumos
            consumos.append(intervalo["consumo"])

        # Calculamos el consumo medio
        consumoMediana = np.median(consumos)

        # Creación de objeto PruebaConsumo
        pruebaConsumoLocal = PruebaConsumoLocal(
            userName=user.username,
            name=name,
            category=category,
            device=device,
            tipoPrueba=tipoPrueba,
            socket=enchufe,
            timeTotal=timeTotal,
            consumoMedio=consumoMediana,
            dateTime=str(datetime.now())
        )

        print("Prueba de consumo: ", pruebaConsumoLocal.json())

        # Guarda el objeto en la base de datos
        client.pruebaConsumoLocal.insert_one(pruebaConsumoLocal.dict())

        
        # Apagar las bombillas
        async with httpx.AsyncClient() as cliente:
            body = {
                "entity_id": "script.eb19"
            }
            response = await cliente.post(url, headers=headers, json=body)
            response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
        
        if category == "climate":
            # Apagar termostatos
            async with httpx.AsyncClient() as cliente:
                body = {
                    "entity_id": "script.ts7" # Apaga termostatos
                }
                response = await cliente.post(url, headers=headers, json=body)
                response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error

        if category == "camera":
            async with httpx.AsyncClient() as cliente:
                body = {
                    "entity_id": "script.c1" # Apaga cámaras
                }
                response = await cliente.post(url, headers=headers, json=body)
                response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
                
        return pruebaConsumoLocal
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def calculate_average_consumption(duration: int, headers: dict, enchufe: str) -> tuple[float, List[float], List[float], List[float], List[float]]:
    print("Esperando 10 segundos...")
    await sleep(10)
    
    print("Calculando consumos")

    total_current = 0
    total_voltage = 0
    total_energy = 0
    total_power = 0

    list_current = []
    list_voltage = []
    list_energy = []
    list_power = []

    start_time = time.time()
    while time.time() - start_time < duration:
        async with httpx.AsyncClient() as client:
            # Petición para obtener el current
            response_current = await client.get(CURRENT_URL, headers=headers)
            response_current.raise_for_status()
            current = response_current.json()["state"]

            # Petición para obtener el voltage
            response_voltage = await client.get(VOLTAGE_URL, headers=headers)
            response_voltage.raise_for_status()
            voltage = response_voltage.json()["state"]

            # Petición para obtener el energy
            response_energy = await client.get(ENERGY_URL, headers=headers)
            response_energy.raise_for_status()
            energy = response_energy.json()["state"]

            # Petición para obtener el power
            response_power = await client.get(POWER_URL, headers=headers)
            response_power.raise_for_status()
            power = response_power.json()["state"]

        if enchufe == "switch.athom_smart_plug_v2_9d8b76_smart_plug_v2":
            # Restar los valores E20
            current = float(current) - EB20_CURRENT
            voltage = float(voltage)
            energy = float(energy) - EB20_ENERGY
        else:
            current = float(current)
            voltage = float(voltage)
            energy = float(energy)

        # Acumular los valores
        list_current.append(current)
        list_voltage.append(voltage)
        list_energy.append(energy)
        list_power.append(power)

        total_current += current
        total_voltage += voltage
        total_energy += energy
        total_power += float(power)

        await sleep(1)

    # Calcular la mediana del consumo de energía
    median_energy = np.median(list_energy)

    return median_energy, list_current, list_voltage, list_energy, list_power
