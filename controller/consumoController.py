### Clase Controller de consumo ###

from typing import List
from fastapi import APIRouter, HTTPException, status
from db.models.PruebaConsumo import PruebaConsumo
from db.schemas.pruebaConsumo import pruebaConsumo_schema, pruebasConsumo_schema
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

# Hacer una prueba de consumo
@app.post("/create", response_model=PruebaConsumo, status_code=status.HTTP_201_CREATED)
async def createPConsumo(pConsumo: PruebaConsumo):

    new_pConsumo = await consumoService.createPConsumo(dict(pConsumo))
    return PruebaConsumo(**new_pConsumo)

    #try:
    #    new_pConsumo = await consumoService.createPConsumo(dict(pConsumo))
    #    return PruebaConsumo(**new_pConsumo)
    #except Exception as e:
    #    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
    
