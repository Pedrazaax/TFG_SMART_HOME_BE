from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.models.user import User
from service import userService

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 999
SECRET = "256576dfohbjpkwmsdga8987098'09òkdfsagsa24142jh1k"

app = APIRouter(prefix="/auth",
                   tags=["Authentication"],
                   responses={status.HTTP_404_NOT_FOUND: {"detail":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])
    
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

    return userService.search_user("username", username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario deshabilitado")

    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = userService.search_user("username", form.username)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")

    if user_db.disabled:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario deshabilitado")

    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {
                    "sub": user_db.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
                    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@app.get("/me")
async def me(user: User = Depends(current_user)):
    return user