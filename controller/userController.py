from fastapi import APIRouter, HTTPException, status, Depends
from controller.auth_usersController import current_user
from db.models.user import User
from db.schemas.user import users_schema
from db.client import client
from bson import ObjectId
from typing import List
from service import userService
from passlib.context import CryptContext

crypt = CryptContext(schemes=["bcrypt"])

app = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={404: {"detail":"No encontrado"}})

@app.get("/", response_model=List[User])
async def users(
    user: User = Depends(current_user)
    ):

    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    

    users = users_schema(client.users.find())
    if len(users) == 0:
         raise HTTPException(status_code = 204, detail="La lista está vacía")
    
    return users

@app.get("/{id}")  # Path
async def user(id: str, user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    return userService.search_user("_id", ObjectId(id))


@app.get("/")  # Query
async def user(id: str, user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    return userService.search_user("_id", ObjectId(id))
    
@app.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def registerUser(user: User):
    
    # Email correcto
    if not (userService.validarEmail(user.email)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El formato del email no es correcto")

    # Usuario existe
    if type(userService.search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    # Comprobar que pwd1 y pwd2 coincidan
    if (user.password != user.pwd2):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Las contraseñas no coinciden")

    # Contraseña segura - Comprobar que tenga mínimo mayuscula, minuscula, número y 8 caracteres
    if len(user.password) < 8 or not any(char.isupper() for char in user.password) or not any(char.islower() for char in user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La contraseña debe contener al menos 8 caracteres, mayúsculas y minúsculas")

    # Encriptar contraseña con bcript (bcript-generator)
    user.password = crypt.hash(user.password)
    user.pwd2 = user.password

    # El servicio guarda el usuario en la bbdd con la contraseña encriptada
    try:
        return await userService.register(user)
    except:
        raise HTTPException(status_code=404, detail="No se ha podido crear el usuario")

@app.put("/update", response_model=User)
async def updateUser(user: User, userReg: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not userReg:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return userService.search_user("_id", ObjectId(user.id))
    
@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str, user: User = Depends(current_user)):
    # Verifica si el usuario está autenticado a través del token JWT en la cabecera
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no autenticado")
    
    found = client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code = 404, detail="No se ha eliminado el usuario")
    
