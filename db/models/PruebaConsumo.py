### Prueba de consumo model ###

from pydantic import BaseModel
from typing import Optional
from db.models.Device import Device

class PruebaConsumo(BaseModel):
    idPrueba: Optional[str]
    tipoDevice: Optional[str]
    idDevice: Optional[str]
    prueba: str
    idSocket: str
    timeTotal:Optional[str]
    consumoMedio:Optional[float]