'''
Nombre controlador: device_controller
Descripción: Este controlador se encarga de gestionar las peticiones relacionadas
con los dispositivos de la aplicación.
'''

import json
from typing import List
from bson import json_util
from bson import ObjectId
from pymongo.errors import PyMongoError
from fastapi import APIRouter, HTTPException, status, Depends
from config.main import SingletonOpenApi
from controller.auth_users_controller import current_user
from db.models.user import User
from db.models.device import Device, Command
from db.schemas.device import device_schema, devices_schema
from db.client import client
from service import device_service

app = APIRouter(prefix="/devices",
                   tags=["Devices"],
                   responses={404: {"detail":"No encontrado"}})

OPEN_API = SingletonOpenApi.get_instance()

# Ver dispositivos
@app.get("/", response_model=List[Device])
async def devices(user: User = Depends(current_user)):
    '''
    Lista todos los dispositivos almacenados en la base de datos.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    devices_list = devices_schema(client.devices.find())
    if len(devices_list) == 0:
        raise HTTPException(status_code= 204, detail="La lista está vacía")
    return devices_list

def serialize_device(device):
    '''
    Serializa un dispositivo para que pueda ser devuelto en una petición.
    '''
    device_dict = json.loads(json_util.dumps(device))
    return device_schema(device_dict)

# Lista de todos los dispositivos TUYA
@app.get("/getList")
async def list_devices(user: User = Depends(current_user)):
    '''
    Lista todos los dispositivos TUYA.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    room = client.rooms.find_one({"name": "None"})
    try:
        respuesta = OPEN_API.get('/v1.3/iot-03/devices')
        devices_list = respuesta['result']['list']
        for device in devices_list:
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
                'model': device['model']
            }

            existing_device = client.devices.find_one({'idDevice': device['id']})
            if existing_device is None:
                device_dict['room'] = room
                client.devices.insert_one(device_dict)
            else:
                update_dict = {}
                for key, value in device_dict.items():
                    if key not in ['name', 'model'] and existing_device.get(key) != value:
                        update_dict[key] = value
                if update_dict:
                    client.devices.update_one(
                        {'_id': existing_device['_id']},
                        {'$set': update_dict}
                        )

        db_devices = list(client.devices.find())
        serialized_devices = [serialize_device(device) for device in db_devices]
        return {"success": True, "devices": serialized_devices}
    except PyMongoError as e:
        return {"success": False, "error": str(e)}

@app.put("/updateDevice")
async def update_device(device: Device, user: User = Depends(current_user)):
    '''
    Actualiza un dispositivo en la base de datos.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    device_dict = dict(device)
    try:
        client.devices.find_one_and_replace({"idDevice": device.id_device}, device_dict)
    except PyMongoError as e:
        return{"error": "No se ha actualizado el dispositivo", "exception": str(e)}
    return await device_service.search_device("idDevice", device.id_device)

# Información de dispositivo
@app.get("/info/{idDevice}")
async def info_device(id_device: str, user: User = Depends(current_user)):
    '''
    Devuelve la información de un dispositivo.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    respuesta = OPEN_API.get(f'/v1.0/iot-03/devices/{id_device}')

    return respuesta

# Estado del dispositivo
@app.get("/status/{idDevice}", response_model=List[Command])
async def state_device(id_device: str, user: User = Depends(current_user)):
    '''
    Devuelve el estado de un dispositivo.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    respuesta = OPEN_API.get(f'/v1.0/iot-03/devices/{id_device}/status')

    #respuesta["result"] --> commands del idDevice Reemplazar en la bbdd Device
    command = respuesta["result"]
    return command

# Estado de varios dispositivos
@app.get("/statusDevices/")
async def state_devices(id_device, user: User = Depends(current_user)):
    '''
    Devuelve el estado de varios dispositivos.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    respuesta = OPEN_API.get(f'/v1.0/iot-03/devices/status?device_ids={id_device}')
    return respuesta

# Video Stream URL
@app.get("/video/{idDevice}")
async def video_stream(id_device: str, user: User = Depends(current_user)):
    '''
    Devuelve la URL de streaming de video de un dispositivo.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    json_type = {"type":"hls"}
    respuesta = OPEN_API.post(f'/v1.0/devices/{id_device}/stream/actions/allocate', json_type)

    url =respuesta["result"]["url"]

    json_url = {
        "url": url
    }

    return json_url


# Control del dispositivo
@app.post("/control", response_model=Device)
async def control_device(device: Device, user: User = Depends(current_user)):
    '''
    Controla un dispositivo.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    # Convertir la lista de comandos a una lista de diccionarios
    commands = [command.dict() for command in device.commands]
    await device_service.no_comillas(commands)

    # Filtrar el diccionario que tiene el código que se quiere obtener
    send_command = [command for command in commands if command.get("code") == device.key]
    print(send_command)

    OPEN_API.post(
        f'/v1.0/iot-03/devices/{device.id_device}/commands',
        {'commands': send_command}
        )

    return device

# Eliminar dispositivo
@app.delete(("/delete/{id}"),status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(_id: str, user: User = Depends(current_user)):
    '''
    Elimina un dispositivo de la base de datos.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    json_id = {
        "idDevice": _id
    }

    found = client.devices.find_one_and_delete(json_id)

    if not found:
        raise HTTPException(status_code = 404, detail="No se ha eliminado el dispositivo")

# Añadir dispositivo
@app.post("/create",status_code=status.HTTP_201_CREATED, response_model=Device)
async def add_device(device:Device, user: User = Depends(current_user)):
    '''
    Añade un dispositivo a la base de datos.
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    
    tipo = type(await device_service.search_device("idDevice", device.id_device))
    if tipo == Device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El dispositivo ya existe"
            )
    
    device_dict = dict(device)
    del device_dict["id"]

    _id = client.devices.insert_one(device_dict).inserted_id
    new_device = device_schema(client.devices.find_one({"_id": ObjectId(_id)}))

    return Device(**new_device)
