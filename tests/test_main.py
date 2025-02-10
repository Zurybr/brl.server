# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.item import Item

client = TestClient(app)

def test_read_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
    # Al iniciar el test, la base "in-memory" debería estar vacía
    assert response.json() == []

def test_create_item():
    item_data = {"name": "Test Item", "description": "A test item"}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]

def test_read_item():
    # Crear un item
    item_data = {"name": "Otro Test", "description": "Descripción de prueba"}
    post_response = client.post("/items/", json=item_data)
    assert post_response.status_code == 200
    created_item = post_response.json()
    item_id = created_item["id"]

    # Leer el item creado
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    fetched_item = get_response.json()
    assert fetched_item["id"] == item_id
    assert fetched_item["name"] == item_data["name"]

def test_read_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_item_model_validation():
    # Validación básica del modelo Item
    data = {"id": 1, "name": "Sample", "description": "Sample description"}
    item = Item(**data)
    assert item.id == 1
    assert item.name == "Sample"
