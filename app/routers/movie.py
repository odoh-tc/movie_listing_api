from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.movie import MovieCreate, MovieUpdate, BaseResponse, SortByEnum
from app.services.auth import get_current_user
from app.db.session import get_db
from app.services.movie_service import (
    create_movie_service,
    get_movie_service,
    get_movies_service,
    update_movie_service,
    delete_movie_service
)
from app.db.models.user import User
from app.utils.logger import logger
from uuid import UUID
from app.utils.rate_limiter import limiter

router = APIRouter()

@router.post("/", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def add_movie(request: Request, movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to add movie: {movie} from user_id: {current_user.id}")
        movie_data = await create_movie_service(db, movie, current_user.id)
        logger.info(f"Movie created successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Movie created successfully", data=movie_data)
    except HTTPException as e:
        logger.error(f"Error in add_movie: {e.detail}")
        raise e

@router.get("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def retrieve_movie(request: Request, movie_id: UUID, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Request to view movie with ID: {movie_id}")
        movie = await get_movie_service(db, movie_id)
        if not movie:
            logger.warning(f"Movie not found with ID: {movie_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        logger.info(f"Movie retrieved with ID: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Movie retrieved successfully", data=movie)
    except HTTPException as e:
        logger.error(f"Error in retrieve_movie: {e.detail}")
        raise e


@router.get("/", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("15/minute")
async def list_movies(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, description="Maximum number of items to return"),
    search: str = Query(None, max_length=100, description="Search term for filtering movies"),
    sort_by: SortByEnum = Query(None, description="Sort criteria"),
    db: Session = Depends(get_db),
):
    
    try:
        logger.debug("Request to view movies list")
        movies = await get_movies_service(db, skip, limit, search, sort_by)
        logger.info(f"Movies list retrieved, count: {len(movies)}")
        return BaseResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Movies retrieved successfully",
            data=movies
        )
    except HTTPException as e:
        logger.error(f"Error in retrieve_movies: {e.detail}")
        raise e



@router.put("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def update_movie(request: Request, movie_id: UUID, movie: MovieUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to update movie ID: {movie_id} with data: {movie}")
        movie_data = await update_movie_service(db, movie_id, movie, current_user.id)
        if not movie_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or you are not authorized to update this movie")
        logger.info(f"Movie updated successfully for ID: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Movie updated successfully", data=movie_data)
    except HTTPException as e:
        logger.error(f"Error in update_movie: {e.detail}")
        raise e

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_movie(request: Request, movie_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to delete movie with ID: {movie_id} from user_id: {current_user.id}")
        success = await delete_movie_service(db, movie_id, current_user.id)
        if not success:
            logger.warning(f"Movie not found or unauthorized delete attempt for movie ID: {movie_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or unauthorized")
        logger.info(f"Movie deleted successfully with ID: {movie_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        logger.error(f"Error in delete_movie: {e.detail}")
        raise e
