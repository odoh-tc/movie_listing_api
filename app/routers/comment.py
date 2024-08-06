from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.comment import CommentCreate, CommentResponse, NestedCommentCreate, BaseResponse
from app.services.auth import get_current_user
from app.db.session import get_db
from app.services.comment_service import (
    create_comment_service,
    get_comments_service,
    create_nested_comment_service
)
from app.db.models.user import User
from app.logger.logger import logger

router = APIRouter()

@router.post("/", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def add_comment_to_movie(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to add comment: {comment} from user_id: {current_user.id}")
        comment_data = await create_comment_service(db, comment, current_user.id)
        logger.info(f"Comment created successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Comment created successfully", data=[comment_data])  # Wrap in list if needed
    except HTTPException as e:
        logger.error(f"Error in add_comment_to_movie: {e.detail}")
        raise e


@router.get("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def view_comments_for_movie(movie_id: UUID, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Request to view comments for movie_id: {movie_id}, skip: {skip}, limit: {limit}")
        comments = await get_comments_service(db, movie_id, skip=skip, limit=limit)
        logger.info(f"Comments retrieved successfully for movie_id: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Comments retrieved successfully", data=comments)
    except HTTPException as e:
        logger.error(f"Error in view_comments_for_movie: {e.detail}")
        raise e

@router.post("/nested", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def add_nested_comment(nested_comment: NestedCommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to add nested comment: {nested_comment} from user_id: {current_user.id}")
        comment_data = await create_nested_comment_service(db, nested_comment, current_user.id)
        logger.info(f"Nested comment created successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Nested comment created successfully", data=[comment_data])  # Wrap in a list
    except HTTPException as e:
        logger.error(f"Error in add_nested_comment: {e.detail}")
        raise e

