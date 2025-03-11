### Clase Service de consumo ###

from fastapi import HTTPException, status
from db.client import client, clientConsumoLocal
from db.models.prueba_consumo import TipoPrueba
from db.models.user import User
from db.schemas.prueba_consumo import prueba_consumo_schema, tipo_prueba_schema, dispositivos_simulador_schema
from asyncio import sleep
from typing import List
from main import open_api_singleton
from service import device_service
import time
from datetime import datetime

openapi = open_api_singleton.get_instance()

async def calculate_average_consumption(device_id: str, duration: int) -> tuple[float, List[float], List[float], List[float]]:
    kwh = 0
    total_current = 0
    total_power = 0
    total_voltage = 0

    list_current = []
    list_power = []
    list_voltage = []

    start_time = time.time()
    while time.time() - start_time < duration:
        response = openapi.get(f'/v1.0/iot-03/devices/status?device_ids={device_id}')
        status = response["result"][0]["status"]
       
        for item in status:
            if item['code'] == 'cur_current':
                # Guardar lista de valores de current
                list_current.append(item['value'])
                total_current += item['value']
            elif item['code'] == 'cur_power':
                #Guardar lista de valores de power
                list_power.append(item['value'])
                total_power += item['value']/10
            elif item['code'] == 'cur_voltage':
                # Guardar lista de valores de voltage
                list_voltage.append(item['value'])
                total_voltage += item['value']/10
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

    return kwh, list_current, list_power, list_voltage

async def create_pconsumo(pConsumo: prueba_consumo_schema):
    pConsumo_dict = dict(pConsumo)
    pConsumo_dict["prueba"] = tipoPrueba_to_dict(pConsumo_dict["prueba"])

    timeTotal = 0
    consumoSuma = 0
    consumoMedio = 0

    # Recorremos la lista de intervalos
    for intervalo in pConsumo_dict["prueba"]["intervaloPrueba"]:

        # Calculamos el tiempo total de la prueba
        timeTotal += intervalo["time"]

        # Inicializamos el dispositivo con su estado
        await device_service.no_comillas(intervalo["status"])
        openapi.post('/v1.0/iot-03/devices/{}/commands'.format(pConsumo_dict["idDevice"]), {'commands': intervalo["status"]})

        # Calcular consumo del intervalo
        intervalo["consumo"], intervalo["current"], intervalo["power"], intervalo["voltage"] = await calculate_average_consumption(pConsumo_dict["idSocket"], intervalo["time"])

        # Sumatorio total de los consumos de todos los intervalos
        consumoSuma += intervalo["consumo"]

        # Apagar el dispositivo
        openapi.post(f'/v1.0/iot-03/devices/{pConsumo_dict["idDevice"]}/commands', {'commands': [{'code': 'switch_led', 'value': False}]})
    
    # Calculamos el consumo medio y lo guardamos en el diccionario junto al tiempo total.
    consumoMedio = consumoSuma/len(pConsumo_dict["prueba"]["intervaloPrueba"])
    pConsumo_dict["timeTotal"] = timeTotal
    pConsumo_dict["consumoMedio"] = consumoMedio

    print(datetime.now())
    now = datetime.now()
    pConsumo_dict["dateTime"] = str(now)

    del pConsumo_dict["idPrueba"]

    id = clientConsumoLocal.PruebasConsumo.insert_one(pConsumo_dict).inserted_id
    new_pConsumo = prueba_consumo_schema(clientConsumoLocal.PruebasConsumo.find_one({"_id": id}))

    return new_pConsumo
    

async def create_tipo_prueba(tPrueba: tipo_prueba_schema):
    tPrueba_dict = tipoPrueba_to_dict(tPrueba)
    del tPrueba_dict["idTipoPrueba"]

    id = client.TipoPrueba.insert_one(tPrueba_dict).inserted_id
    new_tPrueba = tipo_prueba_schema(client.TipoPrueba.find_one({"_id": id}))

    return new_tPrueba

def tipoPrueba_to_dict(tPrueba: TipoPrueba) -> dict:
    tipo_dict = tPrueba.dict()
    tipo_dict["intervaloPrueba"] = [i.dict() for i in tPrueba.intervaloPrueba]
    return tipo_dict

async def delete_pconsumo(id: str):
    try:
        print("ID: ", id)
        print("ID object: ", object(id))
        client.PruebasConsumo.delete_one({"idTipoPrueba": id})
    except Exception as e:
        print("Error (consumoService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_dispositivos_simulador(user: User):
    try:
        print("Listando consumos de los dispositivos para el simulador")

        # Obtiene las pruebas de consumo de la base de datos del usuario
        dispositivosSimulador = dispositivos_simulador_schema(client.simConsumos.find({"userName": user.username}))
    
        if len(dispositivosSimulador) == 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No hay consumos para el simulador")
        else:
            return dispositivosSimulador
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))