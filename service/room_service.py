'''
### Clase Service de Room ###
Descripción: Esta clase contiene los métodos que se encargan 
de gestionar las peticiones de la clase Room.
'''

from bson import ObjectId
from db.client import client
from db.models.room import Room
from db.models.device import Device
from db.schemas.room import room_schema
from fastapi import HTTPException, status

async def search_room(field: str, key):
    '''
    Busca una habitación en la base de datos a partir de un campo y un valor.
    '''
    try:
        room = client.rooms.find_one({field: key})

        if room is None:
            return None

        return Room(**room_schema(room))
    except HTTPException as e:
        print("Error (roomService): ", str(e.detail))
        raise e
    except Exception as e:
        print("Error (roomService): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha encontrado la habitacion"
            ) from e

async def add_room(room: Room):
    '''
    Añade una habitación a la base de datos.
    '''
    try:
        room_dict = dict(room)
        del room_dict["id"]

        # Comprobar que no existe una habitación con el mismo nombre
        if client.rooms.find_one({"name": room_dict["name"]}):
            raise HTTPException(status_code = 400, detail="Ya existe una habitación con ese nombre")

        # Comprobar que el nombre no está vacío
        if room_dict["name"] == "":
            raise HTTPException(status_code = 400, detail="El nombre no puede estar vacío")

        _id = client.rooms.insert_one(room_dict).inserted_id
        new_room = room_schema(client.rooms.find_one({"_id": _id}))

        return Room(**new_room)
    except HTTPException as e:
        print("Error (roomService): ", str(e.detail))
        raise e
    except Exception as e:
        print("Error (roomService): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha podido añadir la habitación"
            ) from e

async def delete_room(_id: str):
    '''
    Elimina una habitación de la base de datos.
    '''
    try:
        default_room = client.rooms.find_one({"name": "None"})
        if default_room["_id"] == ObjectId(_id):
            raise HTTPException(status_code = 400, detail="No se puede eliminar la habitación None")

        found = client.rooms.find_one_and_delete({"_id": ObjectId(_id)})

        if not found:
            raise HTTPException(status_code = 404, detail="No se ha eliminado la habitación")

        # Busca los dispositivos que estén en la habitación eliminada
        # y los pone en la habitación por defecto
        devices = client.devices.find({"room": found})
        for device in devices:
            client.devices.update_one({"_id": device["_id"]}, {"$set": {"room": default_room}})

        return str(found["_id"])

    except HTTPException as e:
        print("Error (roomService): ", str(e.detail))
        raise e
    except Exception as e:
        print("Error (roomService): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha podido eliminar la habitación"
            ) from e

async def set_room(device: Device, room: Room):
    '''
    Asigna una habitación a un dispositivo.
    '''
    try:
        device_dict = dict(device)
        room_dict = dict(room)

        # Buscar la habitación en la base de datos
        room = client.rooms.find_one({"name": room_dict["name"]})

        # En el dispositivo se sustituye la el objeto habitación que pasamos como parámetro
        client.devices.update_one({"idDevice": device_dict["idDevice"]}, {"$set": {"room": room}})

        return client.devices.find_one({"idDevice": device_dict["idDevice"]})
    except HTTPException as e:
        print("Error (roomService): ", str(e.detail))
        raise e
    except Exception as e:
        print("Error (roomService): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha podido añadir el dispositivo"
            ) from e
