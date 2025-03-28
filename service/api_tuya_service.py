'''
### Clase Service de keys API TUYA ###
Descripción: Se encarga de gestionar las API keys de los usuarios.
'''

from db.client import client
from db.models.keys_api import KeysAPI
from db.schemas.keys_api import keys_api_schema
from fastapi import HTTPException, status

async def get_keys_api(username: str):
    '''
    Obtiene las API keys de un usuario.
    Realiza una consulta en la base de datos para buscar 
    las API keys del usuario por su nombre de usuario
    '''
    try:
        keys = client.keysAPI.find_one({"username": username})

        if keys is None:
            return None

        # Convierte los resultados en un objeto KeysAPI utilizando el esquema
        return KeysAPI(**keys_api_schema(keys))

    except Exception as e:
        print("Error al buscar las API keys: ", str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se han encontrado API keys para este usuario"
            ) from e

async def register_keys(keys: KeysAPI):
    '''
    Registra las API keys de un usuario.
    '''
    keys_dict = dict(keys)

    del keys_dict["id"]

    try:
        _id = client.keysAPI.insert_one(keys_dict).inserted_id
        new_keys_api = keys_api_schema(client.keysAPI.find_one({"_id": _id}))
    except Exception as e:
        print("Error al guardar las API keys: ", str(e))
        raise HTTPException(
            status_code=404,
            detail="No se han podido añadir las keys de la API"
            ) from e

    return KeysAPI(**new_keys_api)
