from fastapi import FastAPI, Depends, HTTPException, APIRouter
from crud.user import check_credentials, create_user
from schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
import jwt
import os
from dependencies import get_db, create_access_token, create_refresh_token

SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_si_no_hay_env")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        new_access_token = create_access_token({"sub": username})
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@auth_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(get_db)):
    user = check_credentials(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},  # 'sub' es comúnmente usado para el identificador del usuario
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )
    
    # Devolver el token en el formato esperado por OAuth2
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/register")
async def register(user: UserCreate, db:Session = Depends(get_db)):
    new_user = create_user(db, user)
    if(not new_user):
        raise HTTPException(status_code=400, detail="Invalid data")
    return {"message": "User registered sucessfully"}