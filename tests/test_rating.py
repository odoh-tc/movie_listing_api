from datetime import date
import pytest
from sqlalchemy.orm import Session
from app.db.models.movie import Movie
from app.db.schemas.user import UserCreate
from app.services.auth import register_user
from app.db.schemas.rating import RatingScore


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


def test_create_rating(client, db: Session, auth_headers, test_movie):
    rating_data = {
        "movie_id": str(test_movie.id),
        "score": RatingScore.five_stars,
        "review": "Great movie!"
    }
    response = client.post("/ratings/", json=rating_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["score"] == rating_data["score"]
    assert data["data"]["review"] == rating_data["review"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]


def test_update_rating(client, db: Session, auth_headers, test_movie):
    initial_rating_data = {
        "movie_id": str(test_movie.id),
        "score": RatingScore.four_stars,
        "review": "Good movie."
    }
    updated_rating_data = {
        "movie_id": str(test_movie.id),
        "score": RatingScore.three_stars,
        "review": "Average movie."
    }
    
    response = client.post("/ratings/", json=initial_rating_data, headers=auth_headers)
    assert response.status_code == 201

    response = client.post("/ratings/", json=updated_rating_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["score"] == updated_rating_data["score"]
    assert data["data"]["review"] == updated_rating_data["review"]
    assert "id" in data["data"]
    assert "created_at" in data["data"]


def test_view_ratings_for_movie(client, db: Session, auth_headers, test_movie):
    rating_data = {
        "movie_id": str(test_movie.id),
        "score": RatingScore.five_stars,
        "review": "Great movie!"
    }
    client.post("/ratings/", json=rating_data, headers=auth_headers)
    movie_id = rating_data["movie_id"]
    response = client.get(f"/ratings/{movie_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["data"]["ratings"], list)
    assert len(data["data"]["ratings"]) > 0
    assert data["data"]["ratings"][0]["score"] == rating_data["score"]
    assert data["data"]["ratings"][0]["review"] == rating_data["review"]
    assert "created_at" in data["data"]["ratings"][0]

    assert "aggregated_rating" in data["data"]
    assert data["data"]["aggregated_rating"]["average_score"] is not None


def test_create_rating_exceeding_max_length(client, db: Session, auth_headers, test_movie):
    long_review = "A" * 2001  # Create a review that exceeds the 2000 character limit
    rating_data = {
        "movie_id": str(test_movie.id),
        "score": RatingScore.five_stars,
        "review": long_review
    }
    response = client.post("/ratings/", json=rating_data, headers=auth_headers)
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "String should have at most 2000 characters" in data["detail"][0]["msg"]


def test_create_rating_exceeding_word_count(client, db: Session, auth_headers, test_movie):
    long_review = "word " * 201  # Create a review that exceeds the 200 word limit
    rating_data = {
        "movie_id": str(test_movie.id),
        "score": RatingScore.five_stars,
        "review": long_review
    }
    response = client.post("/ratings/", json=rating_data, headers=auth_headers)
    assert response.status_code == 422  # Unprocessable Entity
    data = response.json()
    assert "Review must not exceed 200 words" in data["detail"][0]["msg"]



def test_unauthorized_rating_creation(client):
    rating_data = {
        "movie_id": "valid-movie-id",
        "score": RatingScore.five_stars,
        "review": "Great movie!"
    }
    response = client.post("/ratings/", json=rating_data)
    assert response.status_code == 401  # Unauthorized
    data = response.json()
    assert "Not authenticated" in data["detail"]


def test_invalid_movie_id(client, auth_headers):
    invalid_movie_id = "00000000-0000-0000-0000-000000000000"
    rating_data = {
        "movie_id": invalid_movie_id,
        "score": RatingScore.five_stars,
        "review": "Great movie!"
    }
    response = client.post("/ratings/", json=rating_data, headers=auth_headers)
    assert response.status_code == 404


def test_invalid_rating_score(client, auth_headers):
    invalid_score = 6  # Assuming the valid scores are 1 through 5
    rating_data = {
        "movie_id":"00000000-0000-0000-0000-000000000000",
        "score": invalid_score,
        "review": "Great movie!"
    }
    response = client.post("/ratings/", json=rating_data, headers=auth_headers)
    assert response.status_code == 422


def test_missing_required_fields(client, auth_headers):
    rating_data = {
        "score": RatingScore.five_stars,
    }
    response = client.post("/ratings/", json=rating_data, headers=auth_headers)
    assert response.status_code == 422 
  

