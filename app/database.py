# database.py para SQLite (la que ya tenías)
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from databases import Database

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
database = Database(DATABASE_URL)
Base = declarative_base()

def init_db():
     # query = text("""
    # CREATE TABLE IF NOT EXISTS items (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL,
    #     description TEXT
    # )
    # """)
    # await database.execute(query)
    metadata.create_all(engine)

# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# database.py para PostgreSQL
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import declarative_base
# from databases import Database

# # Configura estos valores según tu instalación de PostgreSQL
# POSTGRES_USER = "your_user"
# POSTGRES_PASSWORD = "your_password"
# POSTGRES_SERVER = "localhost"
# POSTGRES_PORT = "5432"
# POSTGRES_DB = "your_database"

# DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,  # Verificar conexión antes de usar
#     pool_size=5,         # Número máximo de conexiones en el pool
#     max_overflow=10      # Conexiones adicionales permitidas
# )

# metadata = MetaData()
# database = Database(DATABASE_URL)
# Base = declarative_base()

# def init_db():
#     metadata.create_all(engine)

# # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # ## # # # #
# # # # # database.py para SQL Server con Trust Server Certificate
# # # # from sqlalchemy import create_engine, MetaData
# # # # from sqlalchemy.orm import declarative_base
# # # # from databases import Database
# # # # import urllib.parse

# # # # # Configura estos valores según tu instalación de SQL Server
# # # # SQLSERVER_USER = "your_user"
# # # # SQLSERVER_PASSWORD = "your_password"
# # # # SQLSERVER_SERVER = "your_server"
# # # # SQLSERVER_DB = "your_database"

# # # # # Codificar la contraseña para la URL
# # # # params = urllib.parse.quote_plus(
# # # #     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
# # # #     f"SERVER={SQLSERVER_SERVER};"
# # # #     f"DATABASE={SQLSERVER_DB};"
# # # #     f"UID={SQLSERVER_USER};"
# # # #     f"PWD={SQLSERVER_PASSWORD};"
# # # #     "TrustServerCertificate=yes;"
# # # # )

# # # # DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# # # # engine = create_engine(
# # # #     DATABASE_URL,
# # # #     pool_pre_ping=True,     # Verificar conexión antes de usar
# # # #     pool_size=5,            # Número máximo de conexiones en el pool
# # # #     max_overflow=10,        # Conexiones adicionales permitidas
# # # #     fast_executemany=True   # Optimización para inserciones masivas
# # # # )

# # # # metadata = MetaData()
# # # # database = Database(DATABASE_URL)
# # # # Base = declarative_base()

# # # # def init_db():
# # # #     metadata.create_all(engine)