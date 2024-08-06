from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.movie import MovieCreate, MovieUpdate, BaseResponse
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
from app.logger.logger import logger
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def add_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to add movie: {movie} from user_id: {current_user.id}")
        movie_data = await create_movie_service(db, movie, current_user.id)
        logger.info(f"Movie created successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Movie created successfully", data=movie_data)
    except HTTPException as e:
        logger.error(f"Error in add_movie: {e.detail}")
        raise e

@router.get("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def retrieve_movie(movie_id: UUID, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Request to view movie with ID: {movie_id}")
        movie = await get_movie_service(db, movie_id)
        if not movie:
            logger.warning(f"Movie not found with ID: {movie_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        logger.info(f"Movie retrieved successfully with ID: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Movie retrieved successfully", data=movie)
    except HTTPException as e:
        logger.error(f"Error in view_movie: {e.detail}")
        raise e

@router.get("/", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def list_movies(skip: int = 0, limit: int = 10, search: str = Query(None), db: Session = Depends(get_db)):
    try:
        logger.debug(f"Request to view movies list with skip: {skip}, limit: {limit}, search: {search}")
        movies = await get_movies_service(db, skip, limit, search)
        logger.info("Movies retrieved successfully.")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Movies retrieved successfully", data=movies)
    except HTTPException as e:
        logger.error(f"Error in view_movies: {e.detail}")
        raise e

@router.put("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def update_movie(movie_id: UUID, movie: MovieUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to update movie with ID: {movie_id} from user_id: {current_user.id}")
        updated_movie = await update_movie_service(db, movie_id, movie, current_user.id)
        if not updated_movie:
            logger.warning(f"Movie not found or unauthorized update attempt for movie ID: {movie_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or unauthorized")
        logger.info(f"Movie updated successfully with ID: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Movie updated successfully", data=updated_movie)
    except HTTPException as e:
        logger.error(f"Error in update_movie: {e.detail}")
        raise e

@router.delete("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def delete_movie(movie_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to delete movie with ID: {movie_id} from user_id: {current_user.id}")
        deleted_movie = await delete_movie_service(db, movie_id, current_user.id)
        if not deleted_movie:
            logger.warning(f"Movie not found or unauthorized delete attempt for movie ID: {movie_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or unauthorized")
        logger.info(f"Movie deleted successfully with ID: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Movie deleted successfully", data=deleted_movie)
    except HTTPException as e:
        logger.error(f"Error in delete_movie: {e.detail}")
        raise e
