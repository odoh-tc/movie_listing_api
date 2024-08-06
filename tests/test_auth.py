import pytest
from sqlalchemy.orm import Session
from app.db.schemas.user import UserCreate
from app.services.auth import register_user
from fastapi import status

def test_register_user(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["email"] == user_data["email"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]

def test_login_user(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    register_user(UserCreate(**user_data), db)

    response = client.post("/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == user_data["email"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]


def test_login_with_invalid_credentials(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    register_user(UserCreate(**user_data), db)

    response = client.post("/auth/login", json={"email": "wrongemail@gmail.com", "password": user_data["password"]})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}

def test_register_user_with_existing_email(client, db: Session):
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email already registered"}

def test_login_with_missing_credentials(client):
    response = client.post("/auth/login")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

