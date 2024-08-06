from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserResponse, Token, UserLogin, BaseResponse
from app.services.auth import authenticate_user, register_user, login_for_access_token
from app.db.session import get_db
from app.logger.logger import logger

router = APIRouter()

@router.post("/register", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register endpoint called for user: {user.email}")
    new_user = register_user(user, db)
    user_response = UserResponse.from_orm(new_user)
    return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="User registered successfully", data=user_response)

@router.post("/login", response_model=BaseResponse, status_code=status.HTTP_200_OK)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login endpoint called for user: {user_login.email}")
    user = authenticate_user(user_login.email, user_login.password, db)
    if not user:
        logger.warning(f"Failed login attempt for user: {user_login.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    user_response = UserResponse.from_orm(user)
    return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Login successful", data=user_response)

@router.post("/login/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login endpoint called for user: {form_data.username}")
    return login_for_access_token(form_data.username, form_data.password, db)
