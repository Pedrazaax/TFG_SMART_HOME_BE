from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controller import userController, auth_usersController, deviceController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Iniciar servidor en local: python -m uvicorn app:app --reload
# Documentación Swagger: /docs
# Documentación Redocly: /redoc

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
app.include_router(userController.app)
app.include_router(auth_usersController.app)
app.include_router(deviceController.app)