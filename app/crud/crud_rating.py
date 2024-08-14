from sqlalchemy.orm import Session
from app.db.models.movie import Movie
from app.db.models.rating import Rating
from app.db.schemas.rating import RatingCreate, RatingScore
from typing import List, Optional
from sqlalchemy import func
from app.utils.logger import logger
from sqlalchemy.orm.exc import NoResultFound
from uuid import UUID


def get_user_rating_for_movie(db: Session, user_id: UUID, movie_id: UUID) -> Optional[Rating]:
    return db.query(Rating).filter(Rating.user_id == user_id, Rating.movie_id == movie_id).first()


def create_or_update_rating(db: Session, rating: RatingCreate, user_id: UUID) -> Rating:
    logger.debug(f"Checking for existing rating for user_id: {user_id} and movie_id: {rating.movie_id}")
    movie = db.query(Movie).filter(Movie.id == rating.movie_id).first()
    if not movie:
        logger.error(f"Movie with id {rating.movie_id} not found")
        raise NoResultFound(f"Movie with id {rating.movie_id} not found")
    
    db_rating = get_user_rating_for_movie(db, user_id, rating.movie_id)
    
    if db_rating:
        logger.debug(f"Existing rating found with ID: {db_rating.id}. Updating rating.")
        db_rating.score = rating.score
        db_rating.review = rating.review
        db.commit()
        db.refresh(db_rating)
        logger.info(f"Rating updated with ID: {db_rating.id}")
    else:
        logger.debug(f"No existing rating found. Creating new rating.")
        db_rating = Rating(**rating.dict(), user_id=user_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        logger.info(f"Rating created with ID: {db_rating.id}")

    return db_rating


def get_aggregated_rating(db: Session, movie_id: UUID) -> float:
    avg_rating = db.query(func.avg(Rating.score)).filter(Rating.movie_id == movie_id).scalar()
    return round(avg_rating, 2) if avg_rating is not None else None



def get_ratings(db: Session, movie_id: UUID, skip: int = 0, limit: int = 10, rating_score: RatingScore = None):
    logger.debug(f"Fetching ratings for movie_id: {movie_id} with filter rating_score: {rating_score}") 
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        logger.error(f"Movie with id {movie_id} not found")
        raise NoResultFound(f"Movie with id {movie_id} not found")

    query = db.query(Rating).filter(Rating.movie_id == movie_id)
    
    if rating_score:
        query = query.filter(Rating.score == rating_score)
    
    ratings = query.offset(skip).limit(limit).all()
    aggregated_rating = get_aggregated_rating(db, movie_id)
    logger.info(f"Fetched {len(ratings)} ratings and aggregated rating for movie_id: {movie_id}")
    return ratings, aggregated_rating
