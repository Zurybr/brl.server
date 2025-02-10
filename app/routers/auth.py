# app/routers/auth.py
# from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert
from app.auth import create_access_token, create_refresh_token, get_user_from_token
from app.models.user import UserCreate, get_user_by_username,users_table  # Este es un ejemplo de cómo podrías consultar tu base de datos
from datetime import timedelta
from app.database import database

from app.utils.security import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)



from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

@router.post("/register", response_model=UserCreate)
async def register_user(user: UserCreate):
    # Hashear la contraseña antes de guardarla
    hashed_password = hash_password(user.password)

    query = insert(users_table).values(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    try:
        # Start a transaction
        async with database.transaction():
            await database.execute(query)
            return HTMLResponse(content="<h1>Usuario registrado</h1>") 
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    # except IntegrityError as e:
    #     raise HTTPException(status_code=400, detail=f"Username or email already registered")
    except Exception as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            raise HTTPException(status_code=400, detail="Username already registered")
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validación de las credenciales del usuario (con un ejemplo de base de datos)
    user = await get_user_by_username(form_data.username)  # Reemplaza esto por la consulta real a la base de datos
    print(user.password)
    if user and verify_password(form_data.password, user.password):  # Deberías verificar el password con hashing (NO es recomendable hacerlo como texto plano)
        access_token = create_access_token(data={"sub": form_data.username})
        refresh_token = create_refresh_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "Bearer", "refresh_token": refresh_token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    user = await get_user_from_token(refresh_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    # Crear un nuevo token de acceso usando el nombre de usuario extraído del refresh token
    new_access_token = create_access_token(data={"sub": user})
    return {"access_token": new_access_token, "token_type": "bearer"}
