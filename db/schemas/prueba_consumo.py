'''### Prueba de consumo Schema ###'''

def status_schema(status) -> dict:
    '''Devuelve un diccionario con los valores de un status'''
    return {"code": status["code"],
            "value": status["value"]}

def intervalo_prueba_schema(intervalo) -> dict:
    '''Devuelve un diccionario con los valores de un intervalo'''
    return {"time": intervalo["time"],
            "consumo": intervalo["consumo"],
            "current": intervalo["current"],
            "power": intervalo["power"],
            "voltage": intervalo["voltage"],
            "status": [status_schema(s) for s in intervalo["status"]]}

def tipo_prueba_schema(tipo) -> dict:
    '''Devuelve un diccionario con los valores de un tipo de prueba'''
    return {"idTipoPrueba": str(tipo.get("_id", "N_RANDOM")),
            "nombre": tipo["nombre"],
            "tipoDevice": tipo["tipoDevice"],
            "intervaloPrueba": [intervalo_prueba_schema(i) for i in tipo["intervaloPrueba"]]}


def tipo_pruebas_schema(tipos) -> list:
    '''Devuelve una lista de diccionarios con los valores de los tipos de prueba'''
    return [tipo_prueba_schema(tipo) for tipo in tipos]

def prueba_consumo_schema(p_consumo) -> dict:
    '''Devuelve un diccionario con los valores de una prueba de consumo'''
    return {"idPrueba": str(p_consumo["_id"]),
            "tipoDevice": p_consumo["tipoDevice"],
            "idDevice": p_consumo["idDevice"],
            "prueba": tipo_prueba_schema(p_consumo["prueba"]),
            "idSocket": p_consumo["idSocket"],
            "timeTotal": p_consumo["timeTotal"],
            "dateTime": p_consumo["dateTime"],
            "consumoMedio": p_consumo["consumoMedio"]}

def pruebas_consumo_schema(ps_consumo) -> list:
    '''Devuelve una lista de diccionarios con los valores de las pruebas de consumo'''
    return [prueba_consumo_schema(p_consumo) for p_consumo in ps_consumo]

def tipo_prueba_local_schema(tipo) -> dict:
    '''Devuelve un diccionario con los valores de un tipo de prueba'''
    return {"userName": tipo["userName"],
            "name": tipo["name"],
            "category": tipo["category"],
            "device": tipo["device"],
            "intervalos": tipo["intervalos"]}

def tipos_prueba_local_schema(tipos) -> list:
    '''Devuelve una lista de diccionarios con los valores de los tipos de prueba'''
    return [tipo_prueba_local_schema(tipo) for tipo in tipos]

def prueba_consumo_local_schema(p_consumo) -> dict:
    '''Devuelve un diccionario con los valores de una prueba de consumo'''
    return {"userName": p_consumo["userName"],
            "name": p_consumo["name"],
            "category": p_consumo["category"],
            "device": p_consumo["device"],
            "tipoPrueba": p_consumo["tipoPrueba"],
            "socket": p_consumo["socket"],
            "timeTotal": p_consumo["timeTotal"],
            "dateTime": p_consumo["dateTime"],
            "consumoMedio": p_consumo["consumoMedio"]}

def pruebas_sonsumo_local_schema(ps_consumo) -> list:
    '''Devuelve una lista de diccionarios con los valores de las pruebas de consumo'''
    return [prueba_consumo_local_schema(p_consumo) for p_consumo in ps_consumo]


def dispositivo_simulador_schema(dispositivos_simulador) -> dict:
    '''Devuelve un diccionario con los valores de un dispositivo simulador'''
    return {"userName": dispositivos_simulador["userName"],
        "devices": [str(device) for device in dispositivos_simulador["devices"]],
        "estado": dispositivos_simulador["estado"],
        "consumoMedio": dispositivos_simulador["consumoMedio"],
        "potenciaMedia": dispositivos_simulador["potenciaMedia"],
        "intensidadMedia": dispositivos_simulador["intensidadMedia"],
        "etiqueta": dispositivos_simulador["etiqueta"]
    }

def dispositivos_simulador_schema(dispositivos_simulador) -> list:
    '''Devuelve una lista de diccionarios con los valores de los dispositivos simulador'''
    return [dispositivo_simulador_schema(d_simulador) for d_simulador in dispositivos_simulador]
