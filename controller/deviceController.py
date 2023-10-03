#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from typing import List
from db.models.Device import Device, Command
from db.schemas.device import device_schema, devices_schema
from db.client import client
from main import OpenApiSingleton
from bson import json_util
from service import deviceService

app = APIRouter(prefix="/devices",
                   tags=["Devices"],
                   responses={404: {"detail":"No encontrado"}})

openapi = OpenApiSingleton.get_instance()

# Ver dispositivos
@app.get("/", response_model=List[Device])
async def devices():
    devices = devices_schema(client.devices.find())
    if len(devices) == 0:
        raise HTTPException(status_code= 204, detail="La lista está vacía")
    
    return devices

def serialize_device(device):
    device_dict = json.loads(json_util.dumps(device))
    return device_schema(device_dict)

# Lista de todos los dispositivos TUYA
@app.get("/getList")
async def list_devices():
    try:
        respuesta = openapi.get('/v1.3/iot-03/devices')
        devices = respuesta['result']['list']
        for device in devices:
            device_dict = {
                'name': device['name'],
                'idDevice': device['id'],
                'tipoDevice': device['category_name'],
                'key': '',
                'commands': [],
                'create_time': device['create_time'],
                'update_time': device['update_time'],
                'ip': device['ip'],
                'online': device['online'],
                'model': device['model'],
            }

            existing_device = client.devices.find_one({'idDevice': device['id']})
            if existing_device is None:
                client.devices.insert_one(device_dict)
            else:
                update_dict = {}
                for key, value in device_dict.items():
                    if key not in ['name', 'model'] and existing_device.get(key) != value:
                        update_dict[key] = value
                if update_dict:
                    client.devices.update_one({'_id': existing_device['_id']}, {'$set': update_dict})

        db_devices = list(client.devices.find())
        serialized_devices = [serialize_device(device) for device in db_devices]
        return {"success": True, "devices": serialized_devices}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
# Actualizar dispositivo
@app.put("/updateDevice" .format(Device))
async def updateDevice(device: Device):
    device_dict = dict(device)
    
    try:
        client.devices.find_one_and_replace({"idDevice": device.idDevice}, device_dict)
    except:
        return{"error": "No se ha actualizado el dispositivo"}
    
    return await deviceService.search_device("idDevice", device.idDevice)

# Información de dispositivo
@app.get("/info/{idDevice}")
async def info_device(idDevice: str):
 
    respuesta = openapi.get('/v1.0/iot-03/devices/{}'.format(idDevice))

    return respuesta

# Estado del dispositivo
@app.get("/status/{idDevice}", response_model=List[Command])
async def state_device(idDevice: str):
    respuesta = openapi.get('/v1.0/iot-03/devices/{}/status'.format(idDevice))

    #respuesta["result"] --> commands del idDevice Reemplazar en la bbdd Device
    command = respuesta["result"]
    return command

# Estado de varios dispositivos
@app.get("/statusDevices/")
async def state_devices(idDevices):
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
    await deviceService.no_comillas(commands)

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
    if type(await deviceService.search_device("idDevice", device.idDevice)) == Device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El dispositivo ya existe")
    
    device_dict = dict(device)
    del device_dict["id"]

    id = client.devices.insert_one(device_dict).inserted_id
    new_device = device_schema(client.devices.find_one({"_id": ObjectId(id)}))

    return Device(**new_device)