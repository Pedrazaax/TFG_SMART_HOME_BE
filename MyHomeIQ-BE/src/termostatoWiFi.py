#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from properties import ACCESS_ID, ACCESS_KEY, API_ENDPOINT
import inquirer
import json

#Login en Tuya OpenAPI
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Define las claves del JSON en una lista
keys = ["switch", "child_lock", "temp_set", "eco", "upper_temp"]

# Agrega la opción de salir al final de la lista
keys.append("Salir")

# Define la función para cambiar el valor de una clave
def set_value(key, value):
    commands = {'commands': [{'code': key, 'value': value}]}
    openapi.post('/v1.0/iot-03/devices/{}/commands'.format("bfb14fa2967d0a5f67cql1"), commands)

# Define el menú de opciones
questions = [
  inquirer.List('key',
                message="Seleccione una clave para cambiar su valor:",
                choices=keys,
            ),
  inquirer.Text('value', message="Introduzca el nuevo valor para la clave seleccionada:")
]

# Ejecuta el bucle principal del menú
def remove_quotes(value):
    if value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False
    else:
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
    return value

while True:   
    
    # Get the status of a single device
    response = openapi.get("/v1.0/iot-03/devices/{}/status".format("bfb14fa2967d0a5f67cql1"))
    print(json.dumps(response, indent=4))

    # Get the instruction set of the device
    response = openapi.get("/v1.0/iot-03/devices/{}/functions".format("bfb14fa2967d0a5f67cql1"))
    print("Segunda response")
    print(json.dumps(response, indent=4))

    # Mostrar valor de las keys del dispositivo.
    answers = inquirer.prompt(questions)
    key = answers['key']
    
    # Verifica si el usuario seleccionó la opción de salir
    if key == "Salir":
        break
    value = answers['value']
    value = remove_quotes(value)  
    set_value(key, value)
