#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_usersController import current_user
from db.models.Room import Room
from db.models.Device import Device
from db.client import client
from db.models.user import User
from db.schemas.room import rooms_schema
from service import roomService

app = APIRouter(prefix="/room",
                    tags=["Room"],
                    responses={404: {"detail":"No encontrado"}})

# Listar habitaciones que hay creadas en la base de datos
@app.get("/", response_model=None)
async def rooms(
    user: User = Depends(current_user)
    ):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    

    try:
        rooms = rooms_schema(client.rooms.find())
        if len(rooms) == 0:
            raise HTTPException(status_code = 204, detail="La lista está vacía")
        
        return rooms
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error para listar habitaciones")

# Buscar habitación por id
@app.get("/{id}")
async def room(
    id: str, user: User = Depends(current_user)
    ):

    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    try:
        return await roomService.search_room("_id", ObjectId(id))
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error para buscar habitación")

# Añadir nueva habitación
@app.post("/addRoom", status_code=status.HTTP_201_CREATED)
async def addRoom(
    room: Room, 
    user: User = Depends(current_user)
    ):

    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    try:
        return await roomService.addRoom(room)
    except HTTPException as e: 
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error al añadir una nueva habitación")
    
# Eliminar habitación ya creada
@app.delete("/deleteRoom/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteDevice(id: str, user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    try:
        return await roomService.deleteRoom(id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar la habitación")

# Cambiar la habitación del dispositivo
@app.post("/setRoom", status_code=status.HTTP_200_OK, response_model=Device)
async def setRoom(device: Device, room:Room, user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    try:
        return await roomService.setRoom(device, room)
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error (roomController): ", str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error al cambiar de habitación el dispositivo")
