import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_registration():
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert "id" in response.json()

def test_user_login():
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route_without_token():
    response = client.get("/api/v1/protected")
    assert response.status_code == 401

def test_protected_route_with_invalid_token():
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/api/v1/protected", headers=headers)
    assert response.status_code == 401
