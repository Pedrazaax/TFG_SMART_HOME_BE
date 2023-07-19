### Prueba de consumo model ###

from pydantic import BaseModel
from typing import Optional, Union, List

class Status(BaseModel):
    code: str
    value: Union[bool, int, str]

class IntervaloPrueba(BaseModel):
    idIntervaloPrueba: Optional[str]
    time: int
    consumo: float
    status: List[Status]

class TipoPrueba(BaseModel):
    idTipoPrueba: Optional[str]
    nombre: Optional[str]
    tipoDevice: Optional[str]
    timeTotal: Optional[int]
    intervaloPrueba: List[IntervaloPrueba]

class PruebaConsumo(BaseModel):
    idPrueba: Optional[str]
    tipoDevice: Optional[str]
    idDevice: Optional[str]
    prueba: Optional[TipoPrueba]
    idSocket: str
    timeTotal:Optional[str]
    consumoMedio:Optional[float]