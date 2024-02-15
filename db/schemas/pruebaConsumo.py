### Prueba de consumo Schema ###

def status_schema(status) -> dict:
    return {"code": status["code"],
            "value": status["value"]}

def intervaloPrueba_schema(intervalo) -> dict:
    return {"time": intervalo["time"],
            "consumo": intervalo["consumo"],
            "current": intervalo["current"],
            "power": intervalo["power"],
            "voltage": intervalo["voltage"],
            "status": [status_schema(s) for s in intervalo["status"]]}

def tipoPrueba_schema(tipo) -> dict:
    return {"idTipoPrueba": str(tipo.get("_id", "N_RANDOM")),
            "nombre": tipo["nombre"],
            "tipoDevice": tipo["tipoDevice"],
            "intervaloPrueba": [intervaloPrueba_schema(i) for i in tipo["intervaloPrueba"]]}


def tipoPruebas_schema(tipos) -> list:
    return [tipoPrueba_schema(tipo) for tipo in tipos]

def pruebaConsumo_schema(pConsumo) -> dict:
    return {"idPrueba": str(pConsumo["_id"]),
            "tipoDevice": pConsumo["tipoDevice"],
            "idDevice": pConsumo["idDevice"],
            "prueba": tipoPrueba_schema(pConsumo["prueba"]),
            "idSocket": pConsumo["idSocket"],
            "timeTotal": pConsumo["timeTotal"],
            "dateTime": pConsumo["dateTime"],
            "consumoMedio": pConsumo["consumoMedio"]}
            

def pruebasConsumo_schema(psConsumo) -> list:
    return [pruebaConsumo_schema(pConsumo) for pConsumo in psConsumo]



