'''
### Clase Service de device ###
Descripción: Clase que contiene los métodos necesarios para el manejo de los dispositivos.
'''

from fastapi import HTTPException
from db.client import client
from db.models.Device import Device
from db.schemas.device import device_schema

async def no_comillas(commands):
    '''
    Método para eliminar las comillas de los valores y poder enviarlo a openapi correctamente
    '''
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

async def search_device(field: str, key):
    '''
    Método para buscar device por id
    '''
    try:
        device = client.devices.find_one({field: key})
        if device is None:
            return None

        return Device(**device_schema(device))

    except Exception as e:
        raise HTTPException(
            status_code = 404,
            detail="No se ha encontrado el usuario" + str(e)
            ) from e

def ceck_openapi_response(response):
    '''
    Método para comprobar si la respuesta de openapi es correcta
    '''
    if response.get("code") == 28841002:
        print("Error en la API de Tuya (NO PERMISSION)")
        raise HTTPException(
            status_code = 403,
            detail="No tienes permisos en la API de TUYA"
            )
