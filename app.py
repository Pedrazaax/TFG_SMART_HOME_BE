'''
API RESTful - MyHomeIQ
Descripción: API RESTful para la gestión de dispositivos y usuarios de la aplicación MyHomeIQ
Autor: Carlos Pedraza Antona

Iniciar servidor en local: python -m uvicorn app:app --reload
Documentación Swagger: /docs
Documentación Redocly: /redoc
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import api_tuya_controller, auth_users_controller
from controller import user_controller, historylogs_controller
from controller import local_device_controller, local_measures_controller
from controller import consumo_controller, device_controller
from controller import room_controller

app = FastAPI()

# Configuración CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Routers
#app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_controller.app)
app.include_router(auth_users_controller.app)
app.include_router(device_controller.app)
app.include_router(consumo_controller.app)
app.include_router(api_tuya_controller.app)
app.include_router(room_controller.app)
app.include_router(local_device_controller.app)
app.include_router(local_measures_controller.app)
app.include_router(historylogs_controller.app)
