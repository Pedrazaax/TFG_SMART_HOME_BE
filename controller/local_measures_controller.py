"""
Nombre controlador: local_measures_controller
Descripción: Controlador de las medidas de consumo globales de los dispositivos locales
"""

from fastapi import APIRouter, HTTPException, status, Depends

from service import local_device_service
from db.models.user import User
from controller.auth_users_controller import current_user

app = APIRouter(prefix="/localMeasures",
                     tags=["Local Measures"],
                     responses={404: {"detail":"Not found"}})

@app.get("/updateMeasurementsConsumption")
async def update_measurements(user: User = Depends(current_user)):
    '''
    Actualiza las medidas de consumo globales de los dispositivos locales
    '''
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Usuario no autenticado")
    try:
        pconsumos = await local_device_service.get_pconsumo(user)
        dispositivos = await local_device_service.sort_pconsumos(pconsumos)
        await local_device_service.get_all_global_average_measures(dispositivos)
        await local_device_service.getEEI(dispositivos)
        await local_device_service.save_measures_data(dispositivos)
        return dispositivos
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localMeasuresController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e
    