### Prueba de consumo Schema ###

def status_schema(status) -> dict:
    return {"code": status["code"],
            "value": status["value"]}

def intervaloPrueba_schema(intervalo) -> dict:
    return {"idIntervaloPrueba": intervalo["idIntervaloPrueba"],
            "time": intervalo["time"],
            "consumo": intervalo["consumo"],
            "status": [status_schema(s) for s in intervalo["status"]]}

def tipoPrueba_schema(tipo) -> dict:
    return {"idTipoPrueba": str(tipo["_id"]),
            "nombre": tipo["nombre"],
            "tipoDevice": tipo["tipoDevice"],
            "timeTotal": tipo["timeTotal"],
            "intervaloPrueba": [intervaloPrueba_schema(i) for i in tipo["intervaloPrueba"]]}

def pruebaConsumo_schema(pConsumo) -> dict:
    return {"idPrueba": str(pConsumo["_id"]),
            "tipoDevice": pConsumo["tipoDevice"],
            "idDevice": pConsumo["idDevice"],
            "prueba": tipoPrueba_schema(pConsumo["prueba"]),
            "idSocket": pConsumo["idSocket"],
            "timeTotal": pConsumo["timeTotal"],
            "consumoMedio": pConsumo["consumoMedio"]}

def pruebasConsumo_schema(psConsumo) -> list:
    return [pruebaConsumo_schema(pConsumo) for pConsumo in psConsumo]



