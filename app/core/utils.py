import bcrypt
import datetime
from datetime import timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.models.model import TrafficOfficer
from app.repository.postgres_repository import QueryManager

from app.core.contants import JWT_SECRET
from app.core.contants import ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(data: dict):
    try:
        # valida que exista el usuario
        _instance_user = QueryManager(TrafficOfficer).get({"email": data.get("email")})

        if not _instance_user:
            return {"status": 401, "msg": "ERROR", "data": "Invalid Password or Email"}

        # valida que el password sea correcto
        unhashed_password(data.get("password"), _instance_user.password)

        # crear token
        token = create_jwt_token({"officer_id": _instance_user.id})
        return {"status": 200, "msg": "OK", "data": {"token": token}}

    except Exception as error:
        return {"status": 401, "data": "Invalid Password or Email", "msg": "ERROR"}


def hashed_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def unhashed_password(password, hashed_password) -> dict:
    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        raise Exception({"status": 401, "msg": "Invalid Password or Email"})


def create_jwt_token(data: dict) -> str:
    expiration_time = datetime.datetime.utcnow() + timedelta(hours=1)
    payload = {"exp": expiration_time, **data}
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return token


# Función para verificar y decodificar un token JWT


def verify_jwt_token(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
