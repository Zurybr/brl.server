from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import insert, select, update, delete, text
from app.auth import get_current_user, oauth2_scheme
from app.database import database
from app.models.item import Item, ItemComplete, items_table
from app.models.user import users_table,UserUpdate,UserCreate
from pydantic import BaseModel

router = APIRouter(
    prefix="/items",
    tags=["items"]
)


# Obtener todos los items (SQL en texto)
@router.get("/", response_model=List[ItemComplete])
async def read_items_sql(token: str = Depends(oauth2_scheme)): # <-- Esto se aplica solo al metodo el token
    query = text("SELECT * FROM items")
    results = await database.fetch_all(query)
    return [ItemComplete(**row) for row in results]

#--------------------------------------------SQL ALCHEMY
@router.get("/prueba", response_model=List[ItemComplete])
async def read_items():
    query = select(items_table)  # SELECT * FROM items
    results = await database.fetch_all(query)
    return [ItemComplete(**row._mapping) for row in results]

# Obtener un solo item por ID (SQL en texto)
@router.get("/{item_id}", response_model=ItemComplete)
async def read_item_sql(item_id: int):
    query = text("SELECT * FROM items WHERE id = :id").bindparams(id=item_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemComplete(**result)

#--------------------------------------------SQL ALCHEMY
@router.get("/prueba/{item_id}", response_model=ItemComplete)
async def read_item(item_id: int):
    query = select(items_table).where(items_table.c.id == item_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemComplete(**result._mapping)

# Crear un nuevo item
@router.post("/", response_model=Item)
async def create_item_sql(item: Item):
    query = text("INSERT INTO items (name, description) VALUES (:name, :description)").bindparams(
        name=item.name,
        description=item.description
    )
    # Ejecutar la consulta con los parámetros vinculados
    await database.execute(query)
    # Retornar el objeto item insertado
    return item

#--------------------------------------------SQL ALCHEMY
@router.post("/prueba", response_model=Item)
async def create_item(item: Item):
    query = insert(items_table).values(
        name=item.name,
        description=item.description
    )
    await database.execute(query)
    return item

# @router.post("/prueba", response_model=UserCreate)
# async def create_item(user: UserCreate):
#     query = insert(users_table).values(
#         username=user.username,
#         email=user.email,
#         password=user.password
#     )
#     await database.execute(query)
#     return user

# Actualizar un item por ID (SQL en texto)
@router.put("/{item_id}", response_model=Item)
async def update_item_sql(item_id: int, item: Item):
    query = text("""
                 
            UPDATE items 
            SET name = :name, description = :description 
            WHERE id = :id
        
        """).bindparams(
        id=item_id,
        name=item.name,
        description=item.description
    )
    
    result = await database.execute(query)
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(id=item_id, name=item.name, description=item.description)

#--------------------------------------------SQL ALCHEMY
@router.put("/prueba/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    query = update(items_table).where(items_table.c.id == item_id).values(
        name=item.name,
        description=item.description
    )
    result = await database.execute(query)
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(id=item_id, name=item.name, description=item.description)

# Eliminar un item por ID (SQL en texto)
@router.delete("/{item_id}", response_model=dict)
async def delete_item_sql(item_id: int):
    query = text("DELETE FROM items WHERE id = :id").bindparams(id=item_id)
    result = await database.execute(query)
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

#--------------------------------------------SQL ALCHEMY
@router.delete("/prueba/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    query = delete(items_table).where(items_table.c.id == item_id)
    result = await database.execute(query)
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}