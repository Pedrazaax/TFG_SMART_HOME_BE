from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import client
from bson import ObjectId
from typing import List

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
    return search_user("_id", ObjectId(id))


@app.get("/")  # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
@app.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def registerUser(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(client.users.find_one({"_id": id}))

    return User(**new_user)

@app.put("/update", response_model=User)
async def updateUser(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))
    
@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id: str):
    found = client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code = 404, detail="No se ha eliminado el usuario")

def search_user(field: str, key):
    try:
        user = client.users.find_one({field: key})
        if user is None:
            return None
        
        return User(**user_schema(user))
    
    except:
        raise HTTPException(status_code = 404, detail="No se ha encontrado el usuario")
