import pytest
from sqlalchemy.orm import Session
from app.db.schemas.user import UserCreate
from app.services.auth import register_user
from fastapi import status

@pytest.fixture
def auth_headers(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    register_user(UserCreate(**user_data), db)

    response = client.post("/auth/login/token", data={"username": user_data["email"], "password": user_data["password"]})
    token = response.json()["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == user_data["email"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]


def test_get_current_user_details_without_auth(client):
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_get_current_user_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}