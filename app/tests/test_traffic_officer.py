from fastapi.testclient import TestClient
from config.main import app
import pytest

client = TestClient(app)


def test_create_driver():
    # Datos de prueba
    data = {
        "name": "Agente Test",
        "last_name": "Test 001",
        "nid": "123456789",
        "phone": "400500600",
        "email": "agente12@mail.com",
        "password": "test123?",
    }

    response = client.post("/api/v1/officer", json=data)
    assert response.status_code == 200


# def test_update_create_driver():
#     # Datos de prueba
#     data = {
#         "name": "Agente actualizado",
#         "last_name": "Test update",
#         "phone": "9090909"
#     }

#     response = client.put("/api/v1/officer", json=data)
#     assert response.status_code == 200
