"""
### Clase Service para gestionar las medidas locales y las simulaciones. ###
Description: Este servicio se encarga de gestionar las medidas locales y las simulaciones.
"""

from typing import List, Dict

from fastapi import HTTPException, status
from db.client import client
from db.models.user import User

class LocalMeasuresService:
    """
    Clase servicio para gestionar las medidas locales y las simulaciones.
    """

    async def save_measures_custom(self, user: User, devices: List[Dict]):
        """
        Método para guardar las medidas personalizadas de los dispositivos locales.
        """
        try:
            devices_sim = []
            list_consumption = []
            list_power = []
            list_intensity = []

            for device in devices:
                list_devices = list(client["pruebaConsumoLocal"].find({"device": device["device"]}))
                script = device["estado"]
                devices_sim.append(device["device"])

                for device in list_devices:
                    consumption = self.calculate_con(device, script)
                    power = self.calculate_pot(device, script)
                    intensity = self.calculate_int(device, script)

                    if consumption is not None:
                        list_consumption.append(consumption)
                    if power is not None:
                        list_power.append(power)
                    if intensity is not None:
                        list_intensity.append(intensity)

            dict_measures = self.calculate_measures(list_consumption, list_power, list_intensity)

            simulation_results = {
                "userName": user.username,
                "devices": devices_sim,
                "estado": "Personalizado",
                "consumoMedio": dict_measures.get("consumoMedio"),
                "potenciaMedia": dict_measures.get("potenciaMedia"),
                "intensidadMedia": dict_measures.get("intensidadMedia"),
                "etiqueta": self.calculate_etq(dict_measures)
            }

            print("Resultados: ", simulation_results)
            simulation_results["_id"] = str(client.simConsumos.insert_one(simulation_results).inserted_id)

            return {"simulation_results": simulation_results, "message": "Simulación guardada correctamente"}
        except Exception as e:
            print("Error (LocalMeasuresService): ", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
                ) from e

    def calculate_measures(
            self,
            list_consumption: List[float],
            list_power: List[float],
            list_intensity: List[float]) -> Dict:
        """
        Calcula las medidas globales de consumo, potencia, 
        intensidad y etiqueta de eficiencia energética.
        """
        try:
            if len(list_consumption) != 0 or len(list_power) != 0 or len(list_intensity) != 0:
                total_consumption = sum(list_consumption)/len(list_consumption)
                total_power = sum(list_power)/len(list_power)
                total_intensity = sum(list_intensity)/len(list_intensity)

                return {
                    "consumoMedio": total_consumption,
                    "potenciaMedia": total_power,
                    "intensidadMedia": total_intensity
                }
        except Exception as e:
            print("Error (LocalMeasuresService)(calculate_measures): ", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
                ) from e

    def calculate_con(self, device: Dict, script: str) -> float:
        """
        Calcula el consumo diario promedio para un dispositivo.
        """
        try:
            for intervalo in device["tipoPrueba"]["intervalos"]:
                if script == intervalo["script"]:
                    return intervalo["consumo"]
        except Exception as e:
            print("Error (LocalMeasuresService)(calculate_con): ", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
                ) from e

    def calculate_pot(self, device: Dict, script: str) -> float:
        """
        Calcula la potencia promedio diaria para un dispositivo.
        """
        try:
            list_pot = []
            for intervalo in device["tipoPrueba"]["intervalos"]:
                if script == intervalo["script"]:
                    list_pot = intervalo["power"]

            if len(list_pot) == 0:
                return None

            return sum(list_pot)/len(list_pot)

        except Exception as e:
            print("Error (LocalMeasuresService)(calculate_pot): ", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
                ) from e

    def calculate_int(self, device: Dict, script: str) -> float:
        """
        Calcula la intensidad promedio diaria para un dispositivo.
        """
        try:
            list_int = []
            for intervalo in device["tipoPrueba"]["intervalos"]:
                if script == intervalo["script"]:
                    list_int = intervalo["energy"]

            if len(list_int) == 0:
                return None

            return sum(list_int)/len(list_int)
        except Exception as e:
            print("Error (LocalMeasuresService)(calculate_int): ", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
                ) from e

    def calculate_etq(self, measures: Dict) -> str:
        """
        Calcula la etiqueta de eficiencia energética para un dispositivo.
        """

        return "A"
        