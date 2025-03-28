'''
Nombre de Controlador: user_controller
Descripción: Controlador de usuarios
'''

from typing import List
from bson import ObjectId
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_users_controller import current_user
from db.models.user import User
from db.schemas.user import users_schema
from db.client import client
from service import user_service

crypt = CryptContext(schemes=["bcrypt"])

app = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={404: {"detail":"No encontrado"}})

@app.get("/", response_model=List[User])
async def users(
    user_req: User = Depends(current_user)
    ):
    '''
    Listado de usuarios
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user_req:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    try:
        users_list = users_schema(client.users.find())
        if len(users_list) == 0:
            raise HTTPException(status_code = 204, detail="La lista está vacía")

        return users_list
    except Exception as e:
        print("Error (userController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

@app.get("/{id}")  # Path
async def user(_id: str, user_req: User = Depends(current_user)):
    '''
    Buscar usuario por id
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user_req:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    return user_service.search_user("_id", ObjectId(_id))

@app.get("/")  # Query
async def user_query(_id: str, user_req: User = Depends(current_user)):
    '''
    Buscar usuario por id
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user_req:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    return user_service.search_user("_id", ObjectId(_id))

@app.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_req: User):
    '''
    Registro de usuario
    '''

    # Email correcto
    if not user_service.validar_email(user_req.email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El formato del email no es correcto"
            )

    tipo =type(user_service.search_user("email", user_req.email))
    # Usuario existe
    if tipo == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    # Comprobar que pwd1 y pwd2 coincidan
    if user_req.password != user_req.pwd2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Las contraseñas no coinciden"
            )

    # Contraseña segura - Comprobar que tenga mínimo mayuscula, minuscula, número y 8 caracteres
    if len(user_req.password) < 8 or not any(char.isupper() for char in user_req.password) or not any(char.islower() for char in user_req.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La contraseña debe contener al menos 8 caracteres, mayúsculas y minúsculas"
            )

    # Encriptar contraseña con bcript (bcript-generator)
    user_req.password = crypt.hash(user_req.password)
    user_req.pwd2 = user_req.password

    # El servicio guarda el usuario en la bbdd con la contraseña encriptada
    try:
        return await user_service.register(user_req)
    except Exception as e:
        print("Error (userController): ", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se ha registrado el usuario"
            ) from e

@app.put("/update", response_model=User)
async def update_user(user_req: User, user_log: User = Depends(current_user)):
    '''
    Actualizar usuario
    '''
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user_log:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    user_dict = dict(user_req)
    del user_dict["id"]

    try:
        client.users.find_one_and_replace({"_id": ObjectId(user_req.id)}, user_dict)
    except Exception as e:
        print("Error (userController): ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            ) from e

    return user_service.search_user("_id", ObjectId(user_req.id))

@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(_id: str, user_req: User = Depends(current_user)):
    '''
    Eliminar usuario
    '''

    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user_req:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
            )

    found = client.users.find_one_and_delete({"_id": ObjectId(_id)})

    if not found:
        raise HTTPException(
            status_code = 404,
            detail="No se ha eliminado el usuario"
            )
