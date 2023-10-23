from fastapi import APIRouter, HTTPException, status
from db.models.Room import Room
from db.client import client

app = APIRouter(prefix="/users",
                    tags=["Users"],
                    responses={404: {"detail":"No encontrado"}})

@app.get("/")
async def rooms():
    print("Listar rooms")

@app.get("/{id}")
async def room(id: str):
    print("Query")

@app.post("/addRoom", response_model=Room, status_code=status.HTTP_201_CREATED)
async def addRoom(room: Room):
    print("Añadir room")