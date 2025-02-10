# app/models/user.py
from pydantic import BaseModel, EmailStr
from sqlalchemy import Table, Column, Integer, String, select 
from app.database import metadata,database

# Definición de la tabla en la base de datos
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),  # El username debe ser único
    Column("email", String, unique=True, index=True),     # El email también debe ser único
    Column("password", String),  # La contraseña debe ser guardada de manera segura (con hash)
)

# Pydantic model para la creación de usuario (para recibir los datos de entrada)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Aquí puedes recibir la contraseña en texto plano

# Pydantic model para la respuesta (representación de los datos)
class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # Esto indica que el modelo debe ser compatible con SQLAlchemy

class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str  # Esto es clave para que user.password funcione

    class Config:
        orm_mode = True

# Pydantic model para la actualización de usuario (opcional)
class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str


async def get_user_by_username(username: str):
    query = select(users_table).where(users_table.c.username == username)
    result = await database.fetch_one(query)
    if result is None:
        return None
    return UserInDB(**result._mapping)
    # return {"id": 1, "username": "1234", "email": "algo@algo", "password": "1234"}