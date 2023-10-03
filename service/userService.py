### Clase Service de User ###

from db.client import client
from db.models.user import User
from db.schemas.user import user_schema
from fastapi import HTTPException, status

async def register(user: User, response_model=User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        id = client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(client.users.find_one({"_id": id}))
    except:
        raise HTTPException(status_code=404, detail="No se ha podido crear el usuario")
    
    return User(**new_user)

def search_user(field: str, key):
    try:
        user = client.users.find_one({field: key})
        if user is None:
            return None
        
        return User(**user_schema(user))
    
    except:
        print("Usuario no existe")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")
    
def validarEmail(email: str):
    try:
        valido = True
        nombre, dominio = email.split('@')
        try:
            dom1, dom2 = dominio.split('.',maxsplit = 1)
            if not (len(nombre) >= 5 and dom1 and dom2):
                valido = False
        except ValueError:
            # Dominio no contiene "."
            valido = False
    except ValueError:
        # email no contiene "@"
        valido = False

    return valido