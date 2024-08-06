from datetime import timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.schemas.user import UserCreate, Token, UserLogin
from app.crud.crud_user import create_user, get_user_by_email
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User as DBUser
from app.db.session import get_db
from app.logger.logger import logger
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> DBUser:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            logger.warning("Email not found in token payload.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        user = db.query(DBUser).filter(DBUser.email == email).first()
        if not user:
            logger.warning(f"User not found: {email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        logger.info(f"Authenticated user: {email}")
        return user
    except JWTError:
        logger.exception("JWT decoding error.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def register_user(user: UserCreate, db: Session):
    logger.info(f"Registering user: {user.email}")
    db_user = get_user_by_email(db, user.email)
    if db_user:
        logger.warning(f"Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user)
    logger.info(f"User registered successfully: {user.email}")
    return new_user

def authenticate_user(email: str, password: str, db: Session):
    logger.info(f"Authenticating user: {email}")
    user = get_user_by_email(db, email)
    if not user:
        logger.warning(f"User not found: {email}")
        return False
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Invalid password for user: {email}")
        return False
    logger.info(f"User authenticated successfully: {email}")
    return user

def login_for_access_token(email: str, password: str, db: Session):
    logger.info(f"Login attempt for user: {email}")
    user = authenticate_user(email, password, db)
    if not user:
        logger.warning(f"Failed login attempt for user: {email}")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    logger.info(f"Access token generated for user: {email}")
    return Token(access_token=access_token, token_type="bearer")
