import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Cargar la clave secreta desde las variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # Proporcionar un valor por defecto en caso de que no se haya definido en el .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del access token
REFRESH_TOKEN_EXPIRE_DAYS = 7    # Tiempo de expiración del refresh token

# Usar OAuth2PasswordBearer para obtener el token desde el header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token de acceso con una fecha de expiración"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Usar ahora con zona horaria UTC
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Crea un token de refresco con una fecha de expiración extendida"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # Usar ahora con zona horaria UTC
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Verifica si el token es válido y decodifica su contenido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_user_from_token(token: str):
    """Obtiene el usuario a partir del token JWT"""
    payload = verify_token(token)
    if payload:
        return payload.get("sub")  # El 'sub' es el 'subject' del token (por ejemplo, el id del usuario)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )


# Dependencia de FastAPI para obtener el usuario actual desde el token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependencia de FastAPI para obtener el usuario actual desde el token"""
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user
