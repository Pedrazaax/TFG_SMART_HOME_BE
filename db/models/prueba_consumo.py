'''### Prueba de consumo model ###'''

from typing import Optional, Union, List
from pydantic import BaseModel

class Status(BaseModel):
    '''Modelo para el estado de un dispositivo'''
    code: str
    value: Union[bool, int, str]

class IntervaloPrueba(BaseModel):
    '''Modelo para el intervalo de una prueba'''
    time: int
    consumo: Optional[float]
    current: Optional[List[float]]
    power: Optional[List[float]]
    voltage: Optional[List[float]]
    status: List[Status]

class TipoPrueba(BaseModel):
    '''Modelo para el tipo de prueba'''
    idTipoPrueba: Optional[str]
    nombre: Optional[str]
    tipoDevice: Optional[str]
    intervaloPrueba: List[IntervaloPrueba]

class PruebaConsumo(BaseModel):
    '''Modelo para la prueba de consumo'''
    idPrueba: Optional[str]
    tipoDevice: Optional[str]
    idDevice: Optional[str]
    prueba: Optional[TipoPrueba]
    idSocket: str
    timeTotal: Optional[int]
    consumoMedio:Optional[float]
    dateTime:Optional[str]

# Clases para el tipo de prueba local

class Intervalos(BaseModel):
    '''Modelo para los intervalos de una prueba local'''
    time: int
    script: Optional[str]
    consumo: Optional[float]
    current: Optional[List[float]]
    voltage: Optional[List[float]]
    power: Optional[List[float]]
    energy: Optional[List[float]]

class TipoPruebaLocal(BaseModel):
    '''Modelo para el tipo de prueba local'''
    userName: Optional[str]
    name: Optional[str]
    category: Optional[str]
    device: Optional[str]
    intervalos: List[Intervalos]

class Hub(BaseModel):
    '''Modelo para el hub'''
    be: bool
    pulgadas: int
    rel_ancho: int
    rel_alto: int
    t_pantalla: str

# Clases para Prueba de consumo local

class PruebaConsumoLocal(BaseModel):
    '''Modelo para la prueba de consumo local'''
    userName: Optional[str]
    name: Optional[str]
    category: Optional[str]
    hub: Optional[Hub]
    device: Optional[str]
    tipoPrueba: Optional[TipoPruebaLocal]
    socket: Optional[str]
    timeTotal: Optional[int]
    consumoMedio: Optional[float]
    dateTime: Optional[str]

class DispositivosSimulador(BaseModel):
    '''Modelo para los dispositivos del simulador'''
    userName: Optional[str]
    device: Optional[str]
    estados: List[str]
    consumoMedio: Optional[str]
    potenciaMedia: Optional[str]
    intensidadMedia: Optional[str]
    etiqueta: Optional[str]
