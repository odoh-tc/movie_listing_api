import pytest
from sqlalchemy.orm import Session
from app.db.schemas.user import UserCreate
from app.services.auth import register_user

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
    return {"Authorization": f"Bearer {token}"}

def test_create_movie(client, db: Session, auth_headers):
    movie_data = {
        "title": "Test Movie",
        "description": "This is a test movie description.",
        "duration": 120,
        "release_date": "2024-01-01",
        "poster_url": "https://example.com/poster.jpg"
    }
    response = client.post("/movies/", json=movie_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["title"] == movie_data["title"]
    assert data["data"]["description"] == movie_data["description"]
    assert data["data"]["duration"] == movie_data["duration"]
    assert data["data"]["release_date"] == movie_data["release_date"]
    assert data["data"]["poster_url"] == movie_data["poster_url"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]

def test_view_movie(client, db: Session, auth_headers):
    movie_data = {
        "title": "Test Movie",
        "description": "This is a test movie description.",
        "duration": 120,
        "release_date": "2024-01-01",
        "poster_url": "https://example.com/poster.jpg"
    }
    response = client.post("/movies/", json=movie_data, headers=auth_headers)
    movie_id = response.json()["data"]["id"]

    response = client.get(f"/movies/{movie_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == movie_data["title"]
    assert data["data"]["description"] == movie_data["description"]
    assert data["data"]["duration"] == movie_data["duration"]
    assert data["data"]["release_date"] == movie_data["release_date"]
    assert data["data"]["poster_url"] == movie_data["poster_url"]
    assert data["data"]["id"] == movie_id

def test_view_all_movies(client, db: Session, auth_headers):
    response = client.get("/movies/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"], list)

def test_edit_movie(client, db: Session, auth_headers):
    movie_data = {
        "title": "Test Movie",
        "description": "This is a test movie description.",
        "duration": 120,
        "release_date": "2024-01-01",
        "poster_url": "https://example.com/poster.jpg"
    }
    response = client.post("/movies/", json=movie_data, headers=auth_headers)
    movie_id = response.json()["data"]["id"]

    updated_movie_data = {
        "title": "Updated Test Movie",
        "description": "This is an updated test movie description.",
        "duration": 130,
        "release_date": "2024-02-01",
        "poster_url": "https://example.com/updated_poster.jpg"
    }
    response = client.put(f"/movies/{movie_id}", json=updated_movie_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == updated_movie_data["title"]
    assert data["data"]["description"] == updated_movie_data["description"]
    assert data["data"]["duration"] == updated_movie_data["duration"]
    assert data["data"]["release_date"] == updated_movie_data["release_date"]
    assert data["data"]["poster_url"] == updated_movie_data["poster_url"]
    assert data["data"]["id"] == movie_id

def test_delete_movie(client, db: Session, auth_headers):
    movie_data = {
        "title": "Test Movie",
        "description": "This is a test movie description.",
        "duration": 120,
        "release_date": "2024-01-01",
        "poster_url": "https://example.com/poster.jpg"
    }
    response = client.post("/movies/", json=movie_data, headers=auth_headers)
    movie_id = response.json()["data"]["id"]

    response = client.delete(f"/movies/{movie_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/movies/{movie_id}", headers=auth_headers)
    assert response.status_code == 404
