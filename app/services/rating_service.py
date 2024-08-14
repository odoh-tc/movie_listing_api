import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.crud_rating import create_or_update_rating as crud_create_or_update_rating, get_ratings as crud_get_ratings
from app.db.schemas.rating import RatingCreate, RatingScore, RatingResponse, RatingsWithAggregation, AggregatedRating
from app.utils.logger import logger
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from uuid import UUID

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

async def create_or_update_rating_service(db: Session, rating: RatingCreate, user_id: UUID) -> RatingResponse:
    try:
        logger.debug(f"Service call to create or update rating: {rating} for user_id: {user_id}")
        db_rating = crud_create_or_update_rating(db, rating, user_id)
        logger.info(f"Created or updated rating with ID: {db_rating.id}")
        return RatingResponse.from_orm(db_rating)
    except NoResultFound as e:
        logger.error(f"Error in create_or_update_rating_service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

async def get_ratings_service(db: Session, movie_id: UUID, skip: int = 0, limit: int = 10, rating_score: RatingScore = None) -> RatingsWithAggregation:
    try:
        logger.debug(f"Service call to get ratings for movie_id: {movie_id}, skip: {skip}, limit: {limit}, rating_score: {rating_score}")
        ratings, aggregated_rating = crud_get_ratings(db, movie_id, skip, limit, rating_score)
        logger.info(f"Fetched {len(ratings)} ratings and aggregated rating for movie_id: {movie_id}")
        return RatingsWithAggregation(
            aggregated_rating=AggregatedRating(average_score=aggregated_rating),
            ratings=[RatingResponse.from_orm(rating) for rating in ratings]
        )
    except NoResultFound as e:
        logger.error(f"Error in get_ratings_service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
