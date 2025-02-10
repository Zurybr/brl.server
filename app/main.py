from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.auth import oauth2_scheme
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, text
from app.database import database,init_db
from app.routers import items,auth
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la variable APP_ENV
app_env = os.getenv("APP_ENV", "production")  # "production" es el valor por defecto si no se encuentra APP_ENV

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conectar a la base de datos
    await database.connect()
    # Crear las tablas usando MetaData
    init_db()

    yield
    # Shutdown: Desconectar la base de datos
    await database.disconnect()

# Configurar Swagger UI y ReDoc solo en ambiente de desarrollo
if app_env == "development":
    app = FastAPI(
        title="Proyecto FastAPI de Ejemplo",
        lifespan=lifespan,
        docs_url="/docs",       # URL para Swagger UI (documentación interactiva)
        redoc_url="/redoc",     # URL para ReDoc (otra interfaz de documentación)
        openapi_url="/openapi.json",
        #    dependencies=[Depends(oauth2_scheme)]  # <-- Esto se aplica globalmente
    )
else:
    # En producción, se pueden desactivar los docs para mayor seguridad
    app = FastAPI(
        title="Proyecto FastAPI de Ejemplo",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )

# Incluir routers
app.include_router(items.router)
app.include_router(auth.router) 

# Para ejecutar la aplicación directamente con "python -m app.main"
if __name__ == "__main__":
    print(f"APP_ENV: {app_env}")
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
