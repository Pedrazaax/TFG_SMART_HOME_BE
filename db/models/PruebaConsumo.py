### Prueba de consumo model ###

from pydantic import BaseModel
from typing import Optional, Union, List

class Status(BaseModel):
    code: str
    value: Union[bool, int, str]

class IntervaloPrueba(BaseModel):
    time: int
    consumo: Optional[float]
    current: Optional[List[float]]
    power: Optional[List[float]]
    voltage: Optional[List[float]]
    status: List[Status]

class TipoPrueba(BaseModel):
    idTipoPrueba: Optional[str]
    nombre: Optional[str]
    tipoDevice: Optional[str]
    intervaloPrueba: List[IntervaloPrueba]

class Intervalos(BaseModel):
    time: int
    script: Optional[str]

class TipoPruebaLocal(BaseModel):
    name: Optional[str]
    category: Optional[str]
    device: Optional[str]
    intervalos: List[Intervalos]

class PruebaConsumo(BaseModel):
    idPrueba: Optional[str]
    tipoDevice: Optional[str]
    idDevice: Optional[str]
    prueba: Optional[TipoPrueba]
    idSocket: str
    timeTotal: Optional[int]
    consumoMedio:Optional[float]
    dateTime:Optional[str]