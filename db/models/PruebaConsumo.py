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

class PruebaConsumo(BaseModel):
    idPrueba: Optional[str]
    tipoDevice: Optional[str]
    idDevice: Optional[str]
    prueba: Optional[TipoPrueba]
    idSocket: str
    timeTotal: Optional[int]
    consumoMedio:Optional[float]
    dateTime:Optional[str]

# Clase para el tipo de prueba local

class Intervalos(BaseModel):
    time: int
    script: Optional[str]
    consumo: Optional[float]
    current: Optional[List[float]]
    voltage: Optional[List[float]]
    power: Optional[List[float]]
    energy: Optional[List[float]]

class TipoPruebaLocal(BaseModel):
    userName: Optional[str]
    name: Optional[str]
    category: Optional[str]
    device: Optional[str]
    intervalos: List[Intervalos]

class hub(BaseModel):
    be: bool
    pulgadas: int
    rel_ancho: int
    rel_alto: int
    t_pantalla: str

# Clase para Prueba de consumo local
class PruebaConsumoLocal(BaseModel):
    userName: Optional[str]
    name: Optional[str]
    category: Optional[str]
    hub: Optional[hub]
    device: Optional[str]
    tipoPrueba: Optional[TipoPruebaLocal]
    socket: Optional[str]
    timeTotal: Optional[int]
    consumoMedio: Optional[float]
    dateTime: Optional[str]

class dispositivosSimulador(BaseModel):
    userName: Optional[str]
    device: Optional[str]
    estado: Optional[str]
    consumoMedio: Optional[str]
    potenciaMedia: Optional[str]
    intensidadMedia: Optional[str]
    etiqueta: Optional[str]