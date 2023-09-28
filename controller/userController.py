from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import client
from bson import ObjectId
from typing import List
from service import userService

app = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={404: {"detail":"No encontrado"}})

@app.get("/", response_model=List[User])
async def users():
    users = users_schema(client.users.find())
    if len(users) == 0:
         raise HTTPException(status_code = 204, detail="La lista está vacía")
    
    return users

@app.get("/{id}")  # Path
async def user(id: str):
    return userService.search_user("_id", ObjectId(id))


@app.get("/")  # Query
async def user(id: str):
    return userService.search_user("_id", ObjectId(id))
    
@app.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def registerUser(user: User):
    # Email correcto
    if not (userService.validarEmail(user.email)):
        raise HTTPException(status_code=404, detail="El formato del email no es correcto")

    # Usuario existe
    if type(userService.search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    # Contraseña segura
    # Comprobar que tenga mínimo mayuscula, minuscula, número y 8 caracteres
    # Comprobar que pwd1 y pwd2 coincidan
    # Encriptar contraseña con bcript (bcript-generator)
    
    # El servicio guarda el usuario en la bbdd con la contraseña encriptada
    try:
        return await userService.register(user)
    except:
        raise HTTPException(status_code=404, detail="No se ha podido crear el usuario")

@app.put("/update", response_model=User)
async def updateUser(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return userService.search_user("_id", ObjectId(user.id))
    
@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str):
    found = client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code = 404, detail="No se ha eliminado el usuario")
