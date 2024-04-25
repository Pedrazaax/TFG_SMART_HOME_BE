### Clase Service de dispositivos locales ###

from db.models.user import User
from fastapi import HTTPException, status
from db.client import client
from bson import ObjectId
import httpx

async def save_homeAssistant(token: str, dominio: str, user: User):
    try:
        # Crear tupla homeAssistant
        homeAssistant = (token, dominio)

        # Comprueba si el usuario tiene ya token y dominio
        if user.homeAssistant is not None:
            # Elimina la tupla que tenga guardada
            user.homeAssistant.clear()
        else:
            # Guarda la nueva tupla guardando el token y dominio
            user.homeAssistant = homeAssistant
            client.users.update_one({"_id": ObjectId(user.id)}, {"$set": {"homeAssistant": user.homeAssistant}})

    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def validate_domain(dominio: str):
    try:
        # Declaración de flag de tipo booleano
        flag: bool = True

        # Comprueba que empiece por http:// o https://
        if not dominio.startswith("http://") and not dominio.startswith("https://"):
            print('Dominio', dominio)
            print("Dominio no empieza por http:// o https://")
            flag = False
            
        # Comprueba que después de http:// o https:// haya algún carácter, luego un punto y de nuevo caracter
        if not dominio[7:].split(".")[0] or not dominio[7:].split(".")[1]:
            print('Dominio', dominio)
            print("Dominio no tiene caracteres después de http:// o https://")
            flag = False

        return flag

    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def list_scripts(token: str, dominio: str):
    try:
        print("Listando scripts")
        # Inicialización de HTTP Headers con token bearer
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # URL de la petición GET
        url = f"{dominio}/api/states"

        # Petición GET a la API de Home Assistant
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Esto lanzará una excepción si la respuesta tiene un status code de error
            responseJson = response.json()  # Parsea la respuesta JSON a un objeto Python
            scripts = []
            for item in responseJson:
                if item.get("entity_id") == "script":
                    scripts.append(item)
            return scripts
        
    except Exception as e:
        print("Error (localDeviceService): ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))