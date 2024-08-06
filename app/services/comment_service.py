import json
from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.crud.crud_comment import (
    create_comment as crud_create_comment, 
    get_comments as crud_get_comments, 
    create_nested_comment as crud_create_nested_comment
)
from app.db.schemas.comment import CommentCreate, NestedCommentCreate, CommentResponse
from app.logger.logger import logger


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj) 


async def create_comment_service(db: Session, comment: CommentCreate, user_id: UUID) -> CommentResponse:
    try:
        logger.debug(f"Service call to create comment: {comment} for user_id: {user_id}")
        db_comment = crud_create_comment(db, comment, user_id)
        logger.info(f"Comment created successfully with ID: {db_comment.id}")
        return CommentResponse.from_orm(db_comment)
    except NoResultFound as e:
        logger.error(f"Error in create_comment_service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

async def get_comments_service(db: Session, movie_id: UUID, skip: int = 0, limit: int = 10) -> List[CommentResponse]:
    try:
        logger.debug(f"Service call to get comments for movie_id: {movie_id}, skip: {skip}, limit: {limit}")
        comments = crud_get_comments(db, movie_id, skip, limit)
        logger.info(f"Fetched {len(comments)} comments for movie_id: {movie_id}")
        return [CommentResponse.from_orm(comment) for comment in comments]
    except NoResultFound as e:
        logger.error(f"Error in get_comments_service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


async def create_nested_comment_service(db: Session, nested_comment: NestedCommentCreate, user_id: UUID) -> CommentResponse:
    try:
        logger.debug(f"Service call to create nested comment: {nested_comment} for user_id: {user_id}")
        db_comment = crud_create_nested_comment(db, nested_comment, user_id)
        logger.info(f"Nested comment created successfully with ID: {db_comment.id}")
        return CommentResponse.from_orm(db_comment)
    except NoResultFound as e:
        logger.error(f"Error in create_nested_comment_service: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
