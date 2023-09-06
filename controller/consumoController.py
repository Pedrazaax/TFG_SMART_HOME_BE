### Clase Controller de consumo ###

from typing import List
from fastapi import APIRouter, HTTPException, status
from db.models.PruebaConsumo import PruebaConsumo, TipoPrueba 
from db.schemas.pruebaConsumo import pruebasConsumo_schema, tipoPruebas_schema
from db.client import client
from service import consumoService

app = APIRouter(prefix="/consumo",
                    tags=["Consumo"],
                    responses={404: {"detail": "No encontrado"}})


@app.get("/", response_model=List[PruebaConsumo])
async def pruebasConsumo():
    pruebasConsumo = pruebasConsumo_schema(client.PruebasConsumo.find())
    if len(pruebasConsumo) == 0:
         raise HTTPException(status_code=204, detail="La lista está vacía")

    return pruebasConsumo

@app.get("/getPruebas", response_model=List[TipoPrueba])
async def getTipoPrubas():
    tipoPruebas = tipoPruebas_schema(client.TipoPrueba.find())
    if len(tipoPruebas) == 0:
         raise HTTPException(status_code=204, detail="La lista está vacía")

    return tipoPruebas

# Hacer una prueba de consumo
@app.post("/create", response_model=PruebaConsumo, status_code=status.HTTP_201_CREATED)
async def createPConsumo(pConsumo: PruebaConsumo):

    """
    try:
        new_pConsumo = await consumoService.createPConsumo(dict(pConsumo))
        return PruebaConsumo(**new_pConsumo)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    """
    
    new_pConsumo = await consumoService.createPConsumo(pConsumo)
    return PruebaConsumo(**new_pConsumo)

# Crear un nuevo tipo de prueba
@app.post("/createTipoPrueba", response_model=TipoPrueba, status_code=status.HTTP_201_CREATED)
async def createTipoPrueba(tPrueba:TipoPrueba):

    new_tPrueba = await consumoService.createTipoPrueba(tPrueba)
    return TipoPrueba(**new_tPrueba)

    """try:
        new_tPrueba = await consumoService.createTipoPrueba(tPrueba)
        return TipoPrueba(**new_tPrueba)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))"""

# Eliminar prueba de consumo
  
@app.delete(("/delete/{id}"),status_code=status.HTTP_204_NO_CONTENT)
async def deletePConsumo(id: str):

    jsoID = {
        "idDevice": id
    }

    found = client.devices.find_one_and_delete(jsoID)

    if not found:
        raise HTTPException(status_code = 404, detail="No se ha eliminado el dispositivo")