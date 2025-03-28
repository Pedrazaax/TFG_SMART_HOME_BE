'''### Clase Service de consumo ###'''

import time
from datetime import datetime
from asyncio import sleep
from typing import List
from fastapi import HTTPException, status
from db.client import client, clientConsumoLocal
from db.models.prueba_consumo import TipoPrueba
from db.models.user import User
from db.schemas.prueba_consumo import prueba_consumo_schema
from db.schemas.prueba_consumo import tipo_prueba_schema
from db.schemas.prueba_consumo import dispositivos_simulador_schema
from config.main import SingletonOpenApi
from service import device_service

OPEN_API = SingletonOpenApi.get_instance()

async def calculate_average_consumption(
        device_id: str,
        duration: int
        ) -> tuple[float, List[float], List[float], List[float]]:
    '''
    Calcula el consumo medio de un dispositivo en un intervalo de tiempo.
    '''
    kwh = 0
    total_current = 0
    total_power = 0
    total_voltage = 0

    list_current = []
    list_power = []
    list_voltage = []

    start_time = time.time()
    while time.time() - start_time < duration:
        response = OPEN_API.get(f'/v1.0/iot-03/devices/status?device_ids={device_id}')
        status_response = response["result"][0]["status"]

        for item in status_response:
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

async def create_pconsumo(p_consumo: prueba_consumo_schema):
    '''
    Crea una prueba de consumo en la base de datos local. 
    '''
    p_consumo_dict = dict(p_consumo)
    p_consumo_dict["prueba"] = tipo_prueba_to_dict(p_consumo_dict["prueba"])

    time_total = 0
    consumo_suma = 0
    consumo_medio = 0

    # Recorremos la lista de intervalos
    for intervalo in p_consumo_dict["prueba"]["intervaloPrueba"]:

        # Calculamos el tiempo total de la prueba
        time_total += intervalo["time"]

        # Inicializamos el dispositivo con su estado
        await device_service.no_comillas(intervalo["status"])
        OPEN_API.post(
            f'/v1.0/iot-03/devices/{p_consumo_dict["idDevice"]}/commands',
            {'commands': intervalo["status"]}
            )

        # Calcular consumo del intervalo
        intervalo["consumo"], intervalo["current"], intervalo["power"], intervalo["voltage"] = await calculate_average_consumption(p_consumo_dict["idSocket"], intervalo["time"])

        # Sumatorio total de los consumos de todos los intervalos
        consumo_suma += intervalo["consumo"]

        # Apagar el dispositivo
        OPEN_API.post(
            f'/v1.0/iot-03/devices/{p_consumo_dict["idDevice"]}/commands',
            {'commands': [{'code': 'switch_led', 'value': False}]}
            )

    # Calculamos el consumo medio y lo guardamos en el diccionario junto al tiempo total.
    consumo_medio = consumo_suma/len(p_consumo_dict["prueba"]["intervaloPrueba"])
    p_consumo_dict["timeTotal"] = time_total
    p_consumo_dict["consumoMedio"] = consumo_medio

    now = datetime.now()
    p_consumo_dict["dateTime"] = str(now)

    del p_consumo_dict["idPrueba"]

    _id = clientConsumoLocal.PruebasConsumo.insert_one(p_consumo_dict).inserted_id
    new_pconsumo = prueba_consumo_schema(clientConsumoLocal.PruebasConsumo.find_one({"_id": _id}))

    return new_pconsumo

async def create_tipo_prueba(t_prueba: tipo_prueba_schema):
    '''
    Crear un tipo de prueba en la base de datos local.
    '''
    t_prueba_dict = tipo_prueba_to_dict(t_prueba)
    del t_prueba_dict["idTipoPrueba"]

    _id = client.TipoPrueba.insert_one(t_prueba_dict).inserted_id
    new_t_prueba = tipo_prueba_schema(client.TipoPrueba.find_one({"_id": _id}))

    return new_t_prueba

def tipo_prueba_to_dict(t_prueba: TipoPrueba) -> dict:
    '''
    Convierte un objeto de tipo TipoPrueba a un diccionario.
    '''
    tipo_dict = t_prueba.dict()
    tipo_dict["intervaloPrueba"] = [i.dict() for i in t_prueba.intervaloPrueba]
    return tipo_dict

async def delete_pconsumo(_id: str):
    '''
    Elimina una prueba de consumo de la base de datos local.
    '''
    try:
        print("ID: ", _id)
        print("ID object: ", object(_id))
        client.PruebasConsumo.delete_one({"idTipoPrueba": _id})
    except Exception as e:
        print("Error (consumoService): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

async def get_dispositivos_simulador(user: User):
    '''
    Obtiene los consumos de los dispositivos para el simulador.
    '''
    try:
        print("Listando consumos de los dispositivos para el simulador")

        dispositivos_simulador = dispositivos_simulador_schema(
            client.simConsumos.find({"userName": user.username})
            )

        if len(dispositivos_simulador) == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No hay consumos para el simulador"
                )

        return dispositivos_simulador

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (ConsumoService): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e
    