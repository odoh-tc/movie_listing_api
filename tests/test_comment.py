from datetime import date
import pytest
from sqlalchemy.orm import Session
from app.db.models.movie import Movie
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

@pytest.fixture
def test_movie(db: Session):
    movie = Movie(
        title="Test Movie",
        description="A test movie",
        duration=120,
        release_date=date(2024, 1, 1),
        poster_url="https://example.com/poster.jpg"
    )
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
    assert response.status_code == 201
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

    nested_reply_data = {
        "content": "This is a reply to a nested comment.",
        "parent_comment_id": str(data["data"][0]["id"])
    }
    response = client.post("/comments/nested", json=nested_reply_data, headers=auth_headers)
    
    assert response.status_code == 400
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Replies to replies are not allowed."

    response = client.get(f"/comments/{test_movie.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    top_level_comment = data["data"][0]
    assert len(top_level_comment["replies"]) == 1  # Only one direct reply should exist



def test_add_empty_comment(client, db: Session, auth_headers, test_movie):
    comment_data = {
        "content": "",
        "movie_id": str(test_movie.id)
    }
    response = client.post("/comments/", json=comment_data, headers=auth_headers)
    assert response.status_code == 422


def test_add_comment_unauthorized(client, test_movie):
    comment_data = {
        "content": "Unauthorized comment",
        "movie_id": str(test_movie.id)
    }
    response = client.post("/comments/", json=comment_data)
    assert response.status_code == 401



def test_add_multiple_comments(client, db: Session, auth_headers, test_movie):
    for i in range(5):
        comment_data = {
            "content": f"Test comment {i}",
            "movie_id": str(test_movie.id)
        }
        response = client.post("/comments/", json=comment_data, headers=auth_headers)
        assert response.status_code == 201

    response = client.get(f"/comments/{test_movie.id}", headers=auth_headers)
    data = response.json()
    assert len(data["data"]) == 5


def test_add_comment_exceeding_max_length(client, db: Session, auth_headers, test_movie):
    long_comment = "A" * 1001
    comment_data = {
        "content" : long_comment,
        "movie_id": str(test_movie.id)
    }
    response = client.post("/comments/", json=comment_data, headers=auth_headers)
    assert response.status_code == 422
    data = response.json()
    assert "String should have at most 1000 characters" in data["detail"][0]["msg"]


def test_add_comment_to_non_existent_movie(client, db: Session, auth_headers):
    comment_data = {
        "content": "This is a test comment.",
        "movie_id": "00000000-0000-0000-0000-000000000000"
    }
    response = client.post("/comments/", json=comment_data, headers=auth_headers)
    assert response.status_code == 404








