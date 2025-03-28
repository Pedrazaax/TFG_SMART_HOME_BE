'''
Nombre controlador: room_controller
Descripción: CRUD de las habitaciones de la casa
'''

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_users_controller import current_user
from db.models.Room import Room
from db.models.Device import Device
from db.client import client
from db.models.user import User
from db.schemas.room import rooms_schema
from service import room_service

app = APIRouter(prefix="/room",
                    tags=["Room"],
                    responses={404: {"detail":"No encontrado"}})

# Listar habitaciones que hay creadas en la base de datos
@app.get("/", response_model=None)
async def rooms(
    user: User = Depends(current_user)
    ):
    '''
    Listar habitaciones que hay creadas en la base de datos
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        rooms_list = rooms_schema(client.rooms.find())
        if len(rooms_list) == 0:
            raise HTTPException(status_code = 204, detail="La lista está vacía")

        return rooms_list
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error para listar habitaciones"
            ) from e

@app.get("/{id}")
async def room(
    _id: str, user: User = Depends(current_user)
    ):
    '''
    Buscar habitación por id
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return await room_service.search_room("_id", ObjectId(_id))
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error para buscar habitación"
            ) from e

# Añadir nueva habitación
@app.post("/addRoom", status_code=status.HTTP_201_CREATED)
async def add_room(
    room_req: Room,
    user: User = Depends(current_user)
    ):
    '''
    Añadir nueva habitación
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return await room_service.add_room(room_req)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error al añadir una nueva habitación"
            ) from e

@app.delete("/deleteRoom/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(_id: str, user: User = Depends(current_user)):
    '''
    Eliminar habitación
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return await room_service.delete_room(_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar la habitación"
            ) from e

# Cambiar la habitación del dispositivo
@app.post("/setRoom", status_code=status.HTTP_200_OK, response_model=Device)
async def set_room(device: Device, room_req:Room, user: User = Depends(current_user)):
    '''
    Cambiar la habitación del dispositivo
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        return await room_service.set_room(device, room_req)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error al cambiar de habitación el dispositivo"
            ) from e
