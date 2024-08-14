from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from app.db.schemas.rating import RatingCreate, RatingScore, BaseResponse
from app.services.auth import get_current_user
from app.db.session import get_db
from app.services.rating_service import create_or_update_rating_service, get_ratings_service
from app.db.models.user import User
from app.utils.logger import logger
from uuid import UUID
from app.utils.rate_limiter import limiter


router = APIRouter()

@router.post("/", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def rate_movie(request: Request, rating: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.debug(f"Rate movie request: {rating} from user_id: {current_user.id}")
    try:
        rating_data = await create_or_update_rating_service(db, rating, current_user.id)
        logger.info(f"Rating created or updated successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Rating created or updated successfully", data=rating_data)
    except HTTPException as e:
        logger.error(f"Error in rate_movie: {e.detail}")
        raise e
    

@router.get("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_ratings_for_movie(
    request: Request, 
    movie_id: UUID, 
    skip: int = Query(0, ge=0, description="Number of items to skip"), 
    limit: int = Query(10, ge=1, description="Maximum number of items to return"), 
    rating_score: RatingScore = Query(None, description="Filter ratings by specific score"),
    db: Session = Depends(get_db)
):
    logger.debug(f"Get ratings request for movie_id: {movie_id}, skip: {skip}, limit: {limit}, rating_score: {rating_score}")
    try:
        ratings_with_aggregation = await get_ratings_service(db, movie_id, skip=skip, limit=limit, rating_score=rating_score)
        logger.info(f"Ratings and aggregated rating retrieved successfully for movie_id: {movie_id}")
        return BaseResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Ratings retrieved successfully",
            data=ratings_with_aggregation
        )
    except HTTPException as e:
        logger.error(f"Error in get_ratings_for_movie: {e.detail}")
        raise e


