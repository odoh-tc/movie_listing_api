import pytest
from sqlalchemy.orm import Session
from app.db.models.movie import Movie
from app.db.schemas.user import UserCreate
from app.services.auth import register_user

@pytest.fixture
def auth_headers(client, db: Session):
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    register_user(UserCreate(**user_data), db)

    response = client.post("/auth/login/token", data={"username": user_data["email"], "password": user_data["password"]})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_movie(db: Session):
    movie = Movie(title="Test Movie", description="A test movie.")
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

def test_add_comment_to_movie(client, db: Session, auth_headers, test_movie):
    comment_data = {
        "content": "This is a test comment.",
        "movie_id": str(test_movie.id)
    }
    response = client.post("/comments/", json=comment_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["data"][0]["content"] == comment_data["content"]
    assert str(data["data"][0]["movie_id"]) == comment_data["movie_id"]

def test_view_comments_for_movie(client, db: Session, auth_headers, test_movie):
    comment_data = {
        "content": "This is a test comment.",
        "movie_id": str(test_movie.id)
    }
    client.post("/comments/", json=comment_data, headers=auth_headers)

    movie_id = comment_data["movie_id"]
    response = client.get(f"/comments/{movie_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["data"][0]["content"] == comment_data["content"]

def test_add_nested_comment(client, db: Session, auth_headers, test_movie):
    comment_data = {
        "content": "This is a test comment.",
        "movie_id": str(test_movie.id)
    }
    response = client.post("/comments/", json=comment_data, headers=auth_headers)
    data = response.json()
    parent_comment_id = data["data"][0]["id"]

    nested_comment_data = {
        "content": "This is a nested test comment.",
        "parent_comment_id": str(parent_comment_id)
    }
    response = client.post("/comments/nested", json=nested_comment_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["data"][0]["content"] == nested_comment_data["content"]
    assert str(data["data"][0]["parent_comment_id"]) == nested_comment_data["parent_comment_id"]
