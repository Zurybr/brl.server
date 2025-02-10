from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String
from app.database import metadata

# # Definición de la tabla en la base de datos
items_table = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("description", String)
)

# Pydantic model para la respuesta (representación de los datos)
class Item(BaseModel):
    name: str
    description: str

class ItemComplete(Item):
    id: int

