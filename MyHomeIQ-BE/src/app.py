from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controller import userController, auth_usersController

app = FastAPI()

# Iniciar servidor en local: python -m uvicorn app:app --reload
# Documentación Swagger: /docs
# Documentación Redocly: /redoc

#Routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(userController.router)
app.include_router(auth_usersController.router)