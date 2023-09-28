from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "256576dfohbjpkwmsdga8987098'09òkdfsagsa24142jh1k"

app = APIRouter(prefix="/auth",
                   tags=["Authentication"],
                   responses={status.HTTP_404_NOT_FOUND: {"detail":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

#Entidad User
class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool

#Entidad UserDB
class UserDB(User):
    password: str

users_db = {
    "Carlos":{
        "username":"Carlos",
        "name": "Carlos",
        "email": "carlos@gmail.com",
        "disabled": False,
        "password": "$2a$12$phiqpIioDJP5CTxh8wEJRO8VesG1L3MkgV8ECSJPZl71Rth1c5Nmm"
    },
    "Antonio":{
        "username":"Antonio",
        "name": "Antonio",
        "email": "Antonio@gmail.com",
        "disabled": True,
        "password": "$2a$12$phiqpIioDJP5CTxh8wEJRO8VesG1L3MkgV8ECSJPZl71Rth1c5Nmm"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticación invalidas",
                            headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user_db(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario deshabilitado")

    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {
                    "sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
                    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@app.get("/me")
async def me(user: User = Depends(current_user)):
    return user