'''### Device schema ###'''

def room_schema(room):
    '''Esquema de la habitación'''
    return {
        "id": str(room["_id"]),
        "name": room["name"]
    }

def command_schema(command) -> dict:
    '''Esquema de los comandos'''
    return {"code": command.code,
            "value": command.value}

def commands_schema(commands) -> list:
    '''Esquema de la lista de comandos'''
    if commands is None:
        return []
    return [command_schema(command) for command in commands]

def device_schema(device) -> dict:
    '''Esquema del dispositivo'''
    return {
        "id": str(device["_id"]),
        "name": device["name"],
        "idDevice": device["idDevice"],
        "tipoDevice": device["tipoDevice"],
        "key": device["key"],
        "commands": commands_schema(device["commands"]),
        "create_time": device["create_time"],
        "update_time": device["update_time"],
        "ip": device["ip"],
        "online": device["online"],
        "model": device["model"],
        "room": room_schema(device["room"])
    }

def devices_schema(devices) -> list:
    '''Esquema de la lista de dispositivos'''
    return [device_schema(device) for device in devices]
