import pytest
from sqlalchemy.orm import Session
from app.db.schemas.user import UserCreate
from app.services.auth import register_user
from fastapi import status
from datetime import datetime

def test_register_user(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["email"] == user_data["email"]
    assert data["data"]["first_name"] == user_data["first_name"]
    assert data["data"]["last_name"] == user_data["last_name"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]


def test_login_user(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    register_user(UserCreate(**user_data), db)

    response = client.post("/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]
    assert "token_type" in data["data"]
    assert data["data"]["user"]["email"] == user_data["email"]
    assert data["data"]["user"]["first_name"] == user_data["first_name"]
    assert data["data"]["user"]["last_name"] == user_data["last_name"]
    assert "id" in data["data"]["user"]
    assert "created_at" in data["data"]["user"]


def test_login_with_invalid_credentials(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    register_user(UserCreate(**user_data), db)

    response = client.post("/auth/login", json={"email": "wrongemail@gmail.com", "password": user_data["password"]})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_register_user_with_existing_email(client, db: Session):
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email already registered"}

def test_login_with_missing_credentials(client):
    response = client.post("/auth/login")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


def test_verify_user_email(client, db: Session):
    user_data = {
        "email": "verify@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Doe"
    }
    user = register_user(UserCreate(**user_data), db)
    token = user.verification_token

    response = client.get(f"/auth/verify-email?token={token}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Email verified successfully"
    db.refresh(user)
    assert user.is_verified is True
    assert user.verification_token is None


def test_verify_user_email_with_invalid_token(client):
    response = client.get("/auth/verify-email?token=invalidtoken")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid or expired token"}



def test_resend_verification(client, db: Session):
    user_data = {
        "email": "resend@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Doe"
    }
    user = register_user(UserCreate(**user_data), db)

    response = client.post(f"/auth/resend-verification?email={user_data['email']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Verification email resent. Please check your email."
    db.refresh(user)
    assert user.verification_token is not None
    assert user.verification_token_expiry > datetime.utcnow()


def test_resend_verification_for_verified_user(client, db: Session):
    user_data = {
        "email": "verified@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Doe"
    }
    user = register_user(UserCreate(**user_data), db)
    user.is_verified = True
    db.commit()
    response = client.post(f"/auth/resend-verification?email={user_data['email']}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User already verified"}


def test_resend_verification_for_nonexistent_user(client):
    response = client.post(f"/auth/resend-verification?email=nonexistent@example.com")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}

