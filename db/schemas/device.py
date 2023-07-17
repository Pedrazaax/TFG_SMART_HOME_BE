### Device schema ###

def command_schema(command) -> dict:
    return {"code": command.code,
            "value": command.value}

def commands_schema(commands) -> list:
    if commands is None:
            return []
    return [command_schema(command) for command in commands]

def device_schema(device) -> dict:
    return {
        "id": str(device["_id"]),
        "name": device["name"],
        "idDevice": device["idDevice"],
        "tipoDevice": device["tipoDevice"],
        "key": device["key"],
        "commands": commands_schema(device["commands"]),
        "online": device["online"],
        "create_time": device["create_time"],
        "update_time": device["update_time"],
        "ip": device["ip"],
        "online": device["online"],
        "model": device["model"],
    }

def devices_schema(devices) -> list:
    return [device_schema(device) for device in devices]