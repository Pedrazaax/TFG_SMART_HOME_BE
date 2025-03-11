### Clase Service de dispositivos locales ###

from db.models.user import User
from db.models.prueba_consumo import TipoPruebaLocal, PruebaConsumoLocal
from db.schemas.prueba_consumo import tipos_prueba_local_schema, pruebas_sonsumo_local_schema
from fastapi import HTTPException, status
from typing import List
from asyncio import sleep
import time
from datetime import datetime
from db.client import client
from bson import ObjectId
import httpx
import math

# URLs para las peticiones
CURRENT_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_current"
VOLTAGE_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_voltage"
ENERGY_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_energy"
POWER_URL = "https://gsyaiot.me/api/states/sensor.athom_smart_plug_v2_9d8b76_power"

# Valores a restar
EB20_CURRENT = 0.07
EB20_ENERGY = 0
EB20_POWER = 9

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
        tipoPruebaLocal = tipos_prueba_local_schema(client.tipoPruebaLocal.find({"userName": user.username}))

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
        pruebaConsumoLocal = pruebas_sonsumo_local_schema(client.pruebaConsumoLocal.find({"userName": user.username}))
    
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

        # Data:  {'name': 'a', 'category': 'light', 'hub': {'be': True, 'pulgadas': 7, 'rel_ancho': 16, 'rel_alto': 9, 't_pantalla': 'LCD'} ,'device': 'light.smart_bulb_tuya_1', 'tipoPrueba': 'Prueba1', 'socket': 'switch.smart_plug_tuya_1'}

        print("Guardando prueba de consumo")

        # Inicialización de variables
        timeTotal = 0
        consumos = []
        consumoMedio = 0

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
        hub = data.get('hub')
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
        consumoMedio = sum(consumos) / len(consumos)

        # Creación de objeto PruebaConsumo
        pruebaConsumoLocal = PruebaConsumoLocal(
            userName=user.username,
            name=name,
            category=category,
            hub=hub,
            device=device,
            tipoPrueba=tipoPrueba,
            socket=enchufe,
            timeTotal=timeTotal,
            consumoMedio=consumoMedio,
            dateTime=str(datetime.now())
        )

        print("Prueba de consumo: ", pruebaConsumoLocal.json())

        # Guarda el objeto en la base de datos
        client.pruebaConsumoLocal.insert_one(pruebaConsumoLocal.dict())

        
        # Apagar las bombillas
        # async with httpx.AsyncClient() as cliente:
        #    body = {
        #        "entity_id": "script.eb19"
        #    }
        #    response = await cliente.post(url, headers=headers, json=body)
        #    response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
        
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
    print("Esperando 15 segundos...")
    await sleep(15)
    
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
            power = float(power) - EB20_POWER
        else:
            current = float(current)
            voltage = float(voltage)
            energy = float(energy)
            power = float(power)

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
    media_energy = sum(list_energy) / len(list_energy)

    return media_energy, list_current, list_voltage, list_energy, list_power

async def sort_pconsumos(pconsumos):
    # Crear un conjunto para rastrear los valores ya vistos
    dispositivos_vistos = set()
    # Crear una lista para los objetos únicos
    dispositivos = []

    for pconsumo in pconsumos:
            if pconsumo['device'] not in dispositivos_vistos:
                if "hub" not in pconsumo['tipoPrueba']:
                    dispositivos.append({
                        "userName":pconsumo['userName'],
                        "device":pconsumo['device'],
                        "estado":"",
                        "consumoMedio":0,
                        "potenciaMedia":0,
                        "intensidadMedia":0,
                        "etiqueta":"",
                        "pruebas":[pconsumo]
                    })
                    dispositivos_vistos.add(pconsumo['device'])
                else:
                    dispositivos.append({
                        "userName":pconsumo['userName'],
                        "device":pconsumo['device'],
                        "hub":pconsumo['tipoPrueba']['hub'],
                        "estado":"",
                        "consumoMedio":0,
                        "potenciaMedia":0,
                        "intensidadMedia":0,
                        "etiqueta":"",
                        "pruebas":[pconsumo]
                    })
                    dispositivos_vistos.add(pconsumo['device'])
            else:
                for dispositivo in dispositivos:
                    if dispositivo['device'] == pconsumo['device']:
                        dispositivo['pruebas'].append(pconsumo)
                        break
    return dispositivos

async def getAllGlobalAverageMeasures(dispositivos):
    for dispositivo in dispositivos:
        total_energy=0
        total_power=0
        total_current=0
        num_current_values=0
        num_energy_values=0
        num_power_values=0

        for prueba in dispositivo['pruebas']:
            for intervalo in prueba['tipoPrueba']['intervalos']:
                total_energy += sum(intervalo['energy'])
                total_power += sum(intervalo['power'])
                total_current += sum(intervalo['current'])
                num_current_values += len(intervalo['current'])
                num_energy_values += len(intervalo['energy'])
                num_power_values += len(intervalo['power'])
                
        num_pruebas = len(dispositivo['pruebas'])

        dispositivo['consumoMedio'] = total_energy / num_energy_values
        dispositivo['potenciaMedia'] = total_power / num_power_values
        dispositivo['intensidadMedia'] = total_current / num_current_values
        dispositivo['estado'] = "Global"
        del dispositivo['pruebas']
        
    return dispositivos

async def getEEI(dispositivos):
    for dispositivo in dispositivos:
        if(dispositivo['device'].split('.')[0] == 'light'):
            getLightEEI(dispositivo)
        elif(dispositivo['device'].split('.')[0] == 'camera'):
            getCameraEEI(dispositivo)
        elif(dispositivo['device'].split('.')[0] == 'climate'):
            getClimateEEI(dispositivo)
        elif(dispositivo['device'].split('.')[0] == 'media_player'):
            if not isinstance(dispositivo['hub'],bool):
                getMediaPlayerWithScreenEEI(dispositivo)
            else:
                getMediaPlayerWithOutScreenEEI(dispositivo)

def getLightEEI(dispositivo):
    lm = 806
    ftm = 0.926
    eei = (lm / dispositivo['potenciaMedia']) * ftm
    
    if eei >= 210:
        dispositivo['etiqueta'] = "A"
    elif 185 <= eei < 210:
        dispositivo['etiqueta'] = "B"
    elif 160 <= eei < 185:
        dispositivo['etiqueta'] = "C"
    elif 135 <= eei < 160:
        dispositivo['etiqueta'] = "D"
    elif 110 <= eei < 135:
        dispositivo['etiqueta'] = "E"
    elif 85 <= eei < 110:
        dispositivo['etiqueta'] = "F"
    else:
        dispositivo['etiqueta'] = "G"

def getCameraEEI(dispositivo):
    consumoCamarasGeneral = 0.192
    eei = (dispositivo['consumoMedio']/consumoCamarasGeneral)

    if eei <= 0.4:
        dispositivo['etiqueta'] = "A"
    elif 0.4 < eei <= 0.5:
        dispositivo['etiqueta'] = "B"
    elif 0.5 < eei <= 0.6:
        dispositivo['etiqueta'] = "C"
    elif 0.6 < eei <= 0.7:
        dispositivo['etiqueta'] = "D"
    elif 0.7 < eei <= 0.9:
        dispositivo['etiqueta'] = "E"
    elif 0.9 < eei <= 1.1:
        dispositivo['etiqueta'] = "F"
    else:
        dispositivo['etiqueta'] = "G"

def getClimateEEI(dispositivo):
    consumoTermostatosgeneral = 0.036
    eei = (dispositivo['consumoMedio']/consumoTermostatosgeneral)

    if eei <= 0.3:
        dispositivo['etiqueta'] = "A"
    elif 0.3 < eei <= 0.4:
        dispositivo['etiqueta'] = "B"
    elif 0.4 < eei <= 0.55:
        dispositivo['etiqueta'] = "C"
    elif 0.55 < eei <= 0.75:
        dispositivo['etiqueta'] = "D"
    elif 0.75 < eei <= 1:
        dispositivo['etiqueta'] = "E"
    elif 1 < eei <= 1.25:
        dispositivo['etiqueta'] = "F"
    else:
        dispositivo['etiqueta'] = "G"

def getMediaPlayerWithScreenEEI(dispositivo):
    pulgadas_dispositivo = dispositivo['hub']['pulgadas']
    relación_pantalla_ancho = dispositivo['hub']['rel_ancho']
    relación_pantalla_alto = dispositivo['hub']['rel_alto']
    ancho_pantalla = (pulgadas_dispositivo/math.sqrt((relación_pantalla_ancho**2 + relación_pantalla_alto**2)))*relación_pantalla_ancho
    alto_pantalla = (pulgadas_dispositivo/math.sqrt((relación_pantalla_ancho**2 + relación_pantalla_alto**2)))*relación_pantalla_alto
    A = (ancho_pantalla*0.254)*(alto_pantalla*0.254)
    C = 10 if dispositivo['hub']['t_pantalla'] == 'OLED' else 0
    eei = ((dispositivo['potenciaMedia']+1)/(3*((90*math.tan(0.02+0.004*(A-11))+4)+3)+C))

    if eei < 0.3:
        dispositivo['etiqueta'] = "A"
    elif 0.3 <= eei < 0.4:
        dispositivo['etiqueta'] = "B"
    elif 0.4 <= eei < 0.5:
        dispositivo['etiqueta'] = "C"
    elif 0.5 <= eei < 0.6:
        dispositivo['etiqueta'] = "D"
    elif 0.6 <= eei < 0.75:
        dispositivo['etiqueta'] = "E"
    elif 0.75 <= eei <= 1:
        dispositivo['etiqueta'] = "F"
    else:
        dispositivo['etiqueta'] = "G"

def getMediaPlayerWithOutScreenEEI(dispositivo):
    consumoAltavozInteligenteGeneral = 0.12
    eei = (dispositivo['consumoMedio']/consumoAltavozInteligenteGeneral)

    if eei <= 0.3:
        dispositivo['etiqueta'] = "A"
    elif 0.3 < eei <= 0.4:
        dispositivo['etiqueta'] = "B"
    elif 0.4 < eei <= 0.55:
        dispositivo['etiqueta'] = "C"
    elif 0.55 < eei <= 0.75:
        dispositivo['etiqueta'] = "D"
    elif 0.75 < eei <= 1:
        dispositivo['etiqueta'] = "E"
    elif 1 < eei <= 1.25:
        dispositivo['etiqueta'] = "F"
    else:
        dispositivo['etiqueta'] = "G"

async def save_measuresData(data):
    try:
        # Data:  [{"device": "light.smart_bulb_2","estado": "Global","consumoMedio": 0.005231897341888171,"potenciaMedia": 8.997891842346474,"intensidadMedia": 0.0700000000000002,"etiqueta": "G"},{"device": "light.smart_bulb_tuya_1", ...
        print("Guardando mediciones globales de los consumos")

        class mediciones_dispositivo:
            def __init__(self, userName, device, estado, consumoMedio, potenciaMedia, intensidadMedia, etiqueta):
                self.userName = userName
                self.device = device
                self.estado = estado
                self.consumoMedio = consumoMedio
                self.potenciaMedia = potenciaMedia
                self.intensidadMedia = intensidadMedia
                self.etiqueta = etiqueta
            
            def to_dict(self):
                return self.__dict__
        
        mediciones_dispositivos = []
        for medicion in data:
            mediciones_dispositivos.append(mediciones_dispositivo(medicion["userName"], medicion["device"], medicion["estado"], medicion["consumoMedio"], medicion["potenciaMedia"], medicion["intensidadMedia"], medicion["etiqueta"]))
        
        mediciones_dispositivos_dict = [medicion.to_dict() for medicion in mediciones_dispositivos]

        nueva_coleccion = "simConsumos"
        if nueva_coleccion in client.list_collection_names():
            client[nueva_coleccion].delete_many({})
        resultado = client[nueva_coleccion].insert_many(mediciones_dispositivos_dict)
        print("Datos de mediciones globales de los consumos guardados con exito: ", resultado.inserted_ids)
    except Exception as e:
        print("Error (localDeviceService.save_measuresData): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))