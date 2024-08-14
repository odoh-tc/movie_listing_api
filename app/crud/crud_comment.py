from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound
from app.db.models.comment import Comment
from app.db.models.movie import Movie
from app.db.schemas.comment import CommentCreate, NestedCommentCreate
from app.db.models.user import User
from app.utils.logger import logger
from sqlalchemy import desc, asc


def create_comment(db: Session, comment: CommentCreate, user_id: UUID):
    movie = db.query(Movie).filter(Movie.id == comment.movie_id).first()
    if not movie:
        logger.error(f"Movie with id {comment.movie_id} not found")
        raise NoResultFound(f"Movie with id {comment.movie_id} not found")   
    logger.debug(f"Creating comment: {comment} for user_id: {user_id}")
    db_comment = Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    logger.info(f"Comment created with ID: {db_comment.id}")
    return db_comment



def get_comments(db: Session, movie_id: UUID, skip: int = 0, limit: int = 10, sort_order: str = "desc"):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        logger.error(f"Movie with id {movie_id} not found")
        raise NoResultFound(f"Movie with id {movie_id} not found")
    logger.debug(f"Fetching comments for movie_id: {movie_id}, skip: {skip}, limit: {limit}, sort_order: {sort_order}")
   
    order_func = desc if sort_order == "desc" else asc
    
    comments = db.query(Comment)\
        .filter(Comment.movie_id == movie_id, Comment.parent_comment_id == None)\
        .options(joinedload(Comment.replies))\
        .order_by(order_func(Comment.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    logger.info(f"Fetched {len(comments)} comments for movie_id: {movie_id}")
    return comments


def create_nested_comment(db: Session, nested_comment: NestedCommentCreate, user_id: UUID):
    parent_comment = db.query(Comment).filter(Comment.id == nested_comment.parent_comment_id).first()
    if not parent_comment:
        logger.error(f"Parent comment with id {nested_comment.parent_comment_id} not found")
        raise NoResultFound(f"Parent comment with id {nested_comment.parent_comment_id} not found")
        
    if parent_comment.parent_comment_id is not None:
        logger.error(f"Cannot reply to a reply. Comment ID: {parent_comment.id}")
        raise ValueError("Replies to replies are not allowed.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with id {user_id} not found")
        raise NoResultFound(f"User with id {user_id} not found")
    
    logger.debug(f"Creating nested comment: {nested_comment} for user_id: {user_id}")
    db_comment = Comment(**nested_comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    logger.info(f"Nested comment created with ID: {db_comment.id}")
    return db_comment
