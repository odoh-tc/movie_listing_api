from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.logger.logger import logger
from uuid import UUID

def create_user(db: Session, user: UserCreate):
    logger.info("Creating a new user.")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with email: {user.email}")
    return db_user

def get_user_by_email(db: Session, email: str):
    logger.info(f"Fetching user by email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"User found: {email}")
    else:
        logger.info(f"User not found: {email}")
    return user

def get_user(db: Session, user_id: UUID):
    logger.info(f"Fetching user by ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.info(f"User found with ID: {user_id}")
    else:
        logger.info(f"User not found with ID: {user_id}")
    return user
