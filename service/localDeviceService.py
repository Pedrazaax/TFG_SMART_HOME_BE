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
    
async def check_name(name: str, user: User):
    try:
        # Comprueba si el nombre ya existe en la base de datos
        if client.tipoPruebaLocal.find_one({"userName": user.username, "name": name}):
            return True
        else:
            return False

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
        pruebaConsumoLocal = pruebasConsumoLocal_schema(client.pruebaConsumo.find({"userName": user.username}))

        if len(pruebaConsumoLocal) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay pruebas de consumo guardadas")

        return pruebaConsumoLocal
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def save_pconsumo(data: dict, user: User):
    try:

        # Data:  {'name': 'a', 'category': 'light', 'device': 'light.smart_bulb_tuya_1', 'tipoPrueba': 'Prueba1', 'socket': 'switch.smart_plug_tuya_1'}

        print("Guardando prueba de consumo")

        # Inicialización de variables
        timeTotal = 0
        consumoSuma = 0
        consumoMedio = 0

        # Inicialización de HTTP Headers con token bearer
        headers = {
                "Authorization": f"Bearer {user.homeAssistant.tokenHA}",
                "Content-Type": "application/json"
            }

        # URL de la petición GET
        url = f"{user.homeAssistant.dominio}/api/states/{data.get('device')}"

        # Obtiene los datos del JSON
        name = data.get('name')
        category = data.get('category')
        device = data.get('device')
        tipoPrueba = data.get('TipoPrueba')
        enchufe = data.get('enchufe')

        # Obtiene los intervalos del tipo de prueba
        intervalos = []
        for intervalo in tipoPrueba["intervalos"]:
            intervalos.append(intervalo)

        # Recorremos la lista de intervalos del tipo de prueba
        for intervalo in intervalos:
            # Comprueba que el tiempo del intervalo sea mayor que 0
            if intervalo["time"] <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El tiempo del intervalo debe ser mayor que 0")
            
            # Calculamos el tiempo total de la prueba
            timeTotal += intervalo["time"]

            # Inicializamos el dispositivo con su estado
            async with httpx.AsyncClient() as client:
                body = {
                    "entity_id": intervalo["script"]
                }
                response = await client.post(url, headers=headers, json=body)
                response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
                
            # Calcular consumo del intervalo
            intervalo["consumo"], intervalo["current"], intervalo["voltage"] = await calculate_average_consumption(data.get('socket'), intervalo["time"], headers, url)

            # Sumatorio total de los consumos de todos los intervalos
            consumoSuma += intervalo["consumo"]

        # Calculamos el consumo medio
        consumoMedio = consumoSuma / len(intervalos)

        # Creación de objeto PruebaConsumo
        pruebaConsumoLocal = PruebaConsumoLocal(
            userName=user.username,
            name=name,
            category=category,
            device=device,
            tipoPrueba=tipoPrueba,
            enchufe=enchufe,
            intervalos=intervalos,
            timeTotal=timeTotal,
            consumoMedio=consumoMedio,
            dateTime=str(datetime.now())
        )

        # Guarda el objeto en la base de datos
        client.pruebaConsumoLocal.insert_one(pruebaConsumoLocal.dict())

        return pruebaConsumoLocal
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def calculate_average_consumption(socket_id: str, duration: int, headers, url: str) -> tuple[float, List[float], List[float]]:
    kwh = 0
    total_current = 0
    total_voltage = 0

    list_current = []
    list_voltage = []


    start_time = time.time()
    while time.time() - start_time < duration:

        async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers)
                response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
                responseJson = response.json()  # Parsea la respuesta JSON a un objeto Python
        
        status = responseJson["attributes"]

        if status["current"]:
            current = status["current_consumption"]
            voltage = status["voltage"]
            list_current.append(current)
            list_voltage.append(voltage)
            total_current += current
            total_voltage += voltage
        
    await sleep(1)

    average_current = total_current / duration
    # average_power = total_power / duration
    average_voltage = total_voltage / duration

    # Paso de mA -> A
    current = average_current / 1000
    # Calculo de la potencia
    power = current * average_voltage
    # Paso de segundos a horas
    h = duration / 3600
    # Calculo de KWh
    kwh = (power * h) / 1000

    return kwh, list_current, list_voltage
