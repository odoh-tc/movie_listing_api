"""
This module handles movie comments, including adding, viewing, and nesting comments. 
It supports rate limiting and logs all significant actions.
"""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.schemas.comment import CommentCreate, CommentSortOrder, NestedCommentCreate, BaseResponse
from app.services.auth import get_current_user
from app.db.session import get_db
from app.services.comment_service import (
    create_comment_service,
    get_comments_service,
    create_nested_comment_service
)
from app.db.models.user import User
from app.utils.logger import logger
from app.utils.rate_limiter import limiter


router = APIRouter()

@router.post("/", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_comment_to_movie(request: Request, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to add comment: {comment} from user_id: {current_user.id}")
        comment_data = await create_comment_service(db, comment, current_user.id)
        logger.info(f"Comment created successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Comment created successfully", data=[comment_data])  # Wrap in list if needed
    except HTTPException as e:
        logger.error(f"Error in add_comment_to_movie: {e.detail}")
        raise e


@router.get("/{movie_id}", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def view_comments_for_movie(
    request: Request, 
    movie_id: UUID, 
    skip: int = Query(0, ge=0, description="Number of items to skip"), 
    limit: int = Query(10, ge=1, description="Maximum number of items to return"), 
    sort_order: CommentSortOrder = Query(CommentSortOrder.MOST_RECENT, description="Sort order for comments"),
    db: Session = Depends(get_db)
):
    logger.debug(f"Request to view comments for movie_id: {movie_id}, skip: {skip}, limit: {limit}, sort_order: {sort_order}")
    try:
        comments = await get_comments_service(db, movie_id, skip=skip, limit=limit, sort_order=sort_order)
        logger.info(f"Comments retrieved successfully for movie_id: {movie_id}")
        return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Comments retrieved successfully", data=comments)
    except HTTPException as e:
        logger.error(f"Error in view_comments_for_movie: {e.detail}")
        raise e




@router.post("/nested", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_nested_comment(request: Request, nested_comment: NestedCommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        logger.debug(f"Request to add nested comment: {nested_comment} from user_id: {current_user.id}")
        comment_data = await create_nested_comment_service(db, nested_comment, current_user.id)
        logger.info(f"Nested comment created successfully for user_id: {current_user.id}")
        return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="Nested comment created successfully", data=[comment_data])
    except HTTPException as e:
        logger.error(f"Error in add_nested_comment: {e.detail}")
        raise e

