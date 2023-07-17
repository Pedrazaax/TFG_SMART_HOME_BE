### Prueba de consumo Schema ###

def pruebaConsumo_schema(pConsumo) -> dict:
    return {"idPrueba": str(pConsumo["_id"]),
            "tipoDevice": pConsumo["tipoDevice"],
            "idDevice": pConsumo["idDevice"],
            "prueba": pConsumo["prueba"],
            "idSocket": pConsumo["idSocket"],
            "timeTotal": pConsumo["timeTotal"],
            "consumoMedio": pConsumo["consumoMedio"],
            }


def pruebasConsumo_schema(psConsumo) -> list:
    return [pruebaConsumo_schema(pConsumo) for pConsumo in psConsumo]
