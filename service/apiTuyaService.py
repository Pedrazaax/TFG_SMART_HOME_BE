### Clase Service de keys API TUYA ###

import json
from db.client import client
from db.models.KeysAPI import KeysAPI
from db.schemas.KeysAPI import keysAPI_schema
from fastapi import HTTPException, status

async def get_keysAPI(username: str):
    try:
        # Realiza una consulta en la base de datos para buscar las API keys del usuario por su nombre de usuario
        keys = client.keysAPI.find_one({"username": username})

        if keys is None:
            return None
        
        # Convierte los resultados en un objeto KeysAPI utilizando el esquema
        return KeysAPI(**keysAPI_schema(keys))

    except Exception as e:
        print("Error al buscar las API keys: ", str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se han encontrado API keys para este usuario")
    
async def registerKeys(keys: KeysAPI, response_model=KeysAPI):
    keys_dict = dict(keys)
    
    del keys_dict["id"]

    try:
        id = client.keysAPI.insert_one(keys_dict).inserted_id
        new_keysAPI = keysAPI_schema(client.keysAPI.find_one({"_id": id}))
    except Exception as e:
        print("Error al guardar las API keys: ", str(e))
        raise HTTPException(status_code=404, detail="No se han podido añadir las keys de la API")
    
    return KeysAPI(**new_keysAPI)