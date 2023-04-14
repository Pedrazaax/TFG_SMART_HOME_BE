#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Union
from properties import get_openapi_instance

#from db.models.thermostat import Thermostat
#from db.schemas.thermostat import thermostat_schema, thermostats_schema
#from db.client import client

router = APIRouter(prefix="/devices",
                   tags=["Devices"],
                   responses={404: {"detail":"No encontrado"}})

openapi = get_openapi_instance()

class Command(BaseModel):
    code: str
    value: Union[str, int, bool]

class Device(BaseModel):
    idDevice: str
    key: str
    commands: List[Command]

# Control del dispositivo
@router.post("/control", response_model=Device)
async def control_device(device: Device):
    # Convertir la lista de comandos a una lista de diccionarios
    commands = [command.dict() for command in device.commands]
    no_comillas(commands)

    # Filtrar el diccionario que tiene el código que se quiere obtener
    send_command = [command for command in commands if command.get("code") == device.key]

    openapi.post('/v1.0/iot-03/devices/{}/commands'.format(device.idDevice), {'commands': send_command})

    return device

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
