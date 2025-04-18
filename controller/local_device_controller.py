'''
Nombre controlador: local_device_controller
Descripción: Controlador de dispositivos locales
'''

from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_users_controller import current_user
from db.models.user import User
from service import local_device_service

app = APIRouter(prefix="/localDevices",
                     tags=["Local Devices"],
                     responses={404: {"detail":"Not found"}})

# Guardar token de autenticación y dominio proveniente del cliente
@app.post("/saveHA")
async def save_token(data: dict, user: User = Depends(current_user)):
    '''
    Guarda el token de autenticación y dominio de Home Assistant
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    # Comprueba que los datos no estén vacíos
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Datos vacíos")

    # Obtiene el token y el dominio del JSON
    token = data.get('token')
    dominio = data.get('dominio')

    # Comprueba que el token y el dominio existan
    if not token or not dominio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token o dominio faltante"
            )

    # Comprueba que el token sea válido
    if len(token) < 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")

    # Comprueba que el dominio no esté vacío
    if not dominio:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dominio vacío")

    # Comprueba que el dominio sea válido
    if not await local_device_service.validate_domain(dominio, user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dominio inválido")

    try:
        await local_device_service.save_home_assistant(token, dominio, user)
        return user.homeAssistant
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Devolver valor de homeAssistant
@app.get("/getHA")
async def get_ha(user: User = Depends(current_user)):
    '''
    Devuelve el valor de homeAssistant
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return user.homeAssistant
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Guardar tipo de prueba
@app.post("/saveTPrueba")
async def save_tprueba(data: dict, user: User = Depends(current_user)):
    '''
    Guarda un tipo de prueba
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    # Comprueba que los datos no estén vacíos
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Datos vacíos")

    # Comprueba que el nombre, categoría, dispositivo y script existan
    if not data.get('name') or not data.get('category') or not data.get('device') or not data.get('intervalos'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Faltan datos")

    # Comprueba que la category y el device sean la misma categoría.
    category_device = data.get('device').split('.')[0]
    if data.get('category') != category_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría y el dispositivo no coinciden"
            )

    # Comprueba que los tiempos de intervalos no sean 0.
    for intervalo in data.get('intervalos'):
        if intervalo.get('time') == 0 or intervalo.get('script') == "" or intervalo.get('script') is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Intervalos vacíos o con tiempo/script faltante"
                )

    # Comprueba que el nombre no sea repetido
    if await local_device_service.check_name(data.get('name'), user, 'tPrueba'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede repetir el nombre"
            )

    try:
        print("Datos: ", data)
        return await local_device_service.save_tprueba(data, user)
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Eliminar tipo de prueba
@app.delete("/deleteTPrueba/{name}")
async def delete_tprueba(name: str, user: User = Depends(current_user)):
    '''
    Elimina un tipo de prueba
    '''
    print("Nombre: ", name)
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    # Comprueba que el id no esté vacío
    if not name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID vacío")

    try:
        return await local_device_service.delete_tprueba(name, user)
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Eliminar prueba de consumo
@app.delete("/deletePConsumo/{name}")
async def delete_pconsumo(name: str, user: User = Depends(current_user)):
    '''
    Elimina una prueba de consumo
    '''
    print("Nombre: ", name)
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    # Comprueba que el id no esté vacío
    if not name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID vacío")

    try:
        return await local_device_service.delete_pconsumo(name, user)
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Listar Tipos de Prueba
@app.get("/getTPrueba")
async def get_tprueba(user: User = Depends(current_user)):
    '''
    Devuelve los tipos de prueba
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return await local_device_service.get_tprueba(user)
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Guardar prueba de consumo
@app.post("/savePConsumo")
async def save_pconsumo(data: dict, user: User = Depends(current_user)):
    '''
    Guarda una prueba de consumo
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )
    try:
        # Comprueba que los datos no estén vacíos
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Datos vacíos")

        # Comprueba que el nombre, categoría, dispositivo, tipo de prueba y enchufe existan
        if not data.get('name') or not data.get('category') or not data.get('hub') or not data.get('device') or not data.get('tipoPrueba') or not data.get('socket'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Faltan datos")

        # Comprueba que el nombre no sea repetido
        if await local_device_service.check_name(data.get('name'), user, 'pConsumo'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede repetir el nombre"
                )

        return await local_device_service.save_pconsumo(data, user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Listar Pruebas de Consumo
@app.get("/getPConsumo")
async def get_pconsumo(user: User = Depends(current_user)):
    '''
    Devuelve las pruebas de consumo
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return await local_device_service.get_pconsumo(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

# Listar todos los scripts de Home Assistant y dispositivos locales
@app.get("/")
async def get_scripts(user: User = Depends(current_user)):
    '''
    Devuelve todos los scripts de Home Assistant y dispositivos locales
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    # Obtención del token de la base de datos
    token = user.homeAssistant.tokenHA

    # Obtención del dominio de la base de datos
    dominio = user.homeAssistant.dominio

    # Verifica si el token está vacío
    if not token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token no encontrado")

    # Verifica si el dominio está vacío
    if not dominio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")

    try:
        scripts = await local_device_service.list_all(token, dominio)
        return scripts
    except Exception as e:
        print("Error (localDeviceController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e
    