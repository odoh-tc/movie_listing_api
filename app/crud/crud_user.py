from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.utils.logger import logger
from app.utils.email import send_verification_email
from uuid import uuid4
from app.core.config import settings

def create_user(db: Session, user: UserCreate):
    logger.info("Creating a new user.")
    hashed_password = get_password_hash(user.password)
    verification_token = str(uuid4())
    verification_token_expiry = datetime.utcnow() + timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRE_HOURS)

    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        verification_token=verification_token,
        verification_token_expiry=verification_token_expiry
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with email: {user.email}")
    send_verification_email(user.email, verification_token)
    return db_user



def get_user_by_email(db: Session, email: str):
    logger.info(f"Fetching user by email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.info(f"User found: {email}")
    else:
        logger.info(f"User not found: {email}")
    return user

def get_user_by_verification_token(db: Session, token: str) -> User:
    logger.info(f"Fetching user by verification token: {token}")
    token = db.query(User).filter(User.verification_token == token).first()
    if token:
        logger.info(f"User found with verification token: {token}")
    else:
        logger.info(f"User not found with verification token: {token}")
    return token


def get_user(db: Session, user_id: UUID):
    logger.info(f"Fetching user by ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.info(f"User found with ID: {user_id}")
    else:
        logger.info(f"User not found with ID: {user_id}")
    return user
