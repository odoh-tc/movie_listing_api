from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.schemas.user import UserCreate, Token
from app.crud.crud_user import create_user, get_user_by_email, get_user_by_verification_token
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User as DBUser
from app.db.session import get_db
from app.utils.logger import logger
from app.utils.email import send_verification_email

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



def verify_user_email(token: str, db: Session):
    logger.info(f"Verifying user email with token: {token}")
    user = get_user_by_verification_token(db, token)
    
    if not user:
        logger.warning("Invalid or expired token")
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    if user.is_verified:
        logger.warning("User email already verified")
        raise HTTPException(status_code=400, detail="User email already verified")

    current_time = datetime.utcnow()
    logger.info(f"Current time: {current_time}, Token expiry: {user.verification_token_expiry}")
    
    if current_time > user.verification_token_expiry:
        logger.warning("Expired verification token")
        user.verification_token = None
        user.verification_token_expiry = None
        db.commit()
        raise HTTPException(status_code=400, detail="Expired token, please request a new verification email")

    try:
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expiry = None
        db.commit()
        logger.info(f"User verified successfully: {user.email}")
    except Exception as e:
        logger.error(f"Error during user verification: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while verifying the email. Please try again.")
    
    return user



def resend_verification_email(email: str, db: Session):
    logger.info(f"Resending verification email for user: {email}")
    user = get_user_by_email(db, email)
    if not user:
        logger.warning("User not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_verified:
        logger.warning("User email already verified")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already verified")
    
    if user.verification_token and datetime.utcnow() > user.verification_token_expiry:
        user.verification_token = None
        user.verification_token_expiry = None

    verification_token = str(uuid4())
    verification_token_expiry = datetime.utcnow() + timedelta(hours=settings.VERIFICATION_TOKEN_EXPIRE_HOURS)

    user.verification_token = verification_token
    user.verification_token_expiry = verification_token_expiry
    db.commit()
    send_verification_email(user.email, verification_token)
    logger.info(f"Verification email sent to user: {email}")
    return user

