### Clase Service de consumo ###

from db.client import client
from db.models.PruebaConsumo import TipoPrueba
from db.schemas.pruebaConsumo import pruebaConsumo_schema, tipoPrueba_schema
from asyncio import sleep
from typing import List
from main import OpenApiSingleton
import time

openapi = OpenApiSingleton.get_instance()

async def calculate_average_consumption(device_id: str, duration: int) -> float:
    kwh = 0
    total_current = 0
    total_power = 0
    total_voltage = 0
    start_time = time.time()
    while time.time() - start_time < duration:
        response = openapi.get(f'/v1.0/iot-03/devices/status?device_ids={device_id}')
        status = response["result"][0]["status"]
        #print(status)
        for item in status:
            if item['code'] == 'cur_current':
                total_current += item['value']
            elif item['code'] == 'cur_power':
                total_power += item['value']/10
            elif item['code'] == 'cur_voltage':
                total_voltage += item['value']/10
            print(total_current, total_power, total_voltage)
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

    return kwh

async def createPConsumo(pConsumo_dict: pruebaConsumo_schema):
    if pConsumo_dict["tipoDevice"] == 'Light Source':
        if pConsumo_dict["prueba"] == 'Default':
            # Modificar el dispositivo al estado elegido
            openapi.post(f'/v1.0/iot-03/devices/{pConsumo_dict["idDevice"]}/commands', {'commands': [{'code': 'switch_led', 'value': True}]})
            # Calcula durante el tiempo del intervalo el consumo medio
            pConsumo_dict["timeTotal"] = 1
            pConsumo_dict["consumoMedio"] = await calculate_average_consumption(pConsumo_dict["idSocket"], pConsumo_dict["timeTotal"])
            # Modificar el dispositivo al estado del siguiente intervalo o apagarlo.
            openapi.post(f'/v1.0/iot-03/devices/{pConsumo_dict["idDevice"]}/commands', {'commands': [{'code': 'switch_led', 'value': False}]})
    
    del pConsumo_dict["idPrueba"]

    id = client.PruebasConsumo.insert_one(pConsumo_dict).inserted_id
    new_pConsumo = pruebaConsumo_schema(client.PruebasConsumo.find_one({"_id": id}))

    return new_pConsumo

async def createTipoPrueba(tPrueba: tipoPrueba_schema):
    tPrueba_dict = tipoPrueba_to_dict(tPrueba)
    del tPrueba_dict["idTipoPrueba"]

    id = client.TipoPrueba.insert_one(tPrueba_dict).inserted_id
    new_tPrueba = tipoPrueba_schema(client.TipoPrueba.find_one({"_id": id}))

    return new_tPrueba

def tipoPrueba_to_dict(tPrueba: TipoPrueba) -> dict:
    tipo_dict = tPrueba.dict()
    tipo_dict["intervaloPrueba"] = [i.dict() for i in tPrueba.intervaloPrueba]
    return tipo_dict
