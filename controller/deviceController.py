#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from typing import List
from db.models.Device import Device, Command
from db.schemas.device import device_schema, devices_schema
from db.client import client
from properties import get_openapi_instance

#from db.models.thermostat import Thermostat
#from db.schemas.thermostat import thermostat_schema, thermostats_schema
#from db.client import client

app = APIRouter(prefix="/devices",
                   tags=["Devices"],
                   responses={404: {"detail":"No encontrado"}})

openapi = get_openapi_instance()

# Ver dispositivos
@app.get("/", response_model=List[Device])
async def devices():
    devices = devices_schema(client.devices.find())
    if len(devices) == 0:
        raise HTTPException(status_code= 204, detail="La lista está vacía")
    
    return devices

# Estado del dispositivo
@app.get("/status/{idDevice}", response_model=List[Command])
async def state_device(idDevice: str):
    respuesta = openapi.get('/v1.0/iot-03/devices/{}/status'.format(idDevice))

    #respuesta["result"] --> commands del idDevice Reemplazar en la bbdd Device
    command = respuesta["result"]
    return command

# Estado de varios dispositivos
@app.get("/statusDevices/")
async def state_device(idDevices):

    respuesta = openapi.get('/v1.0/iot-03/devices/status?device_ids={}'.format(idDevices))

    return respuesta

# Video Stream URL
@app.get("/video/{idDevice}")
async def videoStream(idDevice: str):

    jsonType = {"type":"hls"}
    respuesta = openapi.post('/v1.0/devices/{}/stream/actions/allocate'.format(idDevice), jsonType)

    url =respuesta["result"]["url"]

    jsonUrl = {
        "url": url
    }

    return jsonUrl


# Control del dispositivo
@app.post("/control", response_model=Device)
async def control_device(device: Device):
    # Convertir la lista de comandos a una lista de diccionarios
    commands = [command.dict() for command in device.commands]
    no_comillas(commands)

    # Filtrar el diccionario que tiene el código que se quiere obtener
    send_command = [command for command in commands if command.get("code") == device.key]

    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(device.idDevice), {'commands': send_command})

    #client.devices.find_one_and_replace(device)

    return device

# Eliminar dispositivo
@app.delete(("/delete/{id}"),status_code=status.HTTP_204_NO_CONTENT)
async def deleteDevice(id: str):

    jsoID = {
        "idDevice": id
    }

    found = client.devices.find_one_and_delete(jsoID)

    if not found:
        raise HTTPException(status_code = 404, detail="No se ha eliminado el dispositivo")

# Añadir dispositivo
@app.post("/create",status_code=status.HTTP_201_CREATED, response_model=Device)
async def add_device(device:Device):
    if type(search_device("idDevice", device.idDevice)) == Device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El dispositivo ya existe")
    
    device_dict = dict(device)
    del device_dict["id"]

    id = client.devices.insert_one(device_dict).inserted_id
    new_device = device_schema(client.devices.find_one({"_id": ObjectId(id)}))

    return Device(**new_device)

# Método para eliminar las comillas de los valores y poder enviarlo a openapi correctamente
def no_comillas(commands):
    for command in commands:
        for key, value in command.items():
            if isinstance(value, str):
                if value == "True":
                    command[key] = True
                elif value == "False":
                    command[key] = False
                else:
                    try:
                        command[key] = int(value)
                    except ValueError:
                        command[key] = value.strip('"')

def search_device(field: str, key):
    try:
        device = client.devices.find_one({field: key})
        if device is None:
            return None
        
        return Device(**device_schema(device))
    
    except:
        raise HTTPException(status_code = 404, detail="No se ha encontrado el usuario")