from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.schemas.user import UserCreate, UserResponse, Token, UserLogin, BaseResponse
from app.services.auth import authenticate_user, register_user, login_for_access_token, resend_verification_email, verify_user_email
from app.db.session import get_db
from app.utils.logger import logger
from app.utils.rate_limiter import limiter


router = APIRouter()

@router.post("/register", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register endpoint called for user: {user.email}")
    new_user = register_user(user, db)
    user_response = UserResponse.from_orm(new_user)
    return BaseResponse(success=True, status_code=status.HTTP_201_CREATED, message="User registered successfully. Please check your email for verification link.", 
                        data=user_response)


@router.post("/login", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def login(request: Request, user_login: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Login endpoint called for user: {user_login.email}")
    user = authenticate_user(user_login.email, user_login.password, db)
    if not user:
        logger.warning(f"Failed login attempt for user: {user_login.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = login_for_access_token(user_login.email, user_login.password, db)
    user_response = UserResponse.from_orm(user)
    return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Login successful",
        data={
            "user": user_response,
            "access_token": token.access_token,
            "token_type": token.token_type
        }
    )

@router.post("/login/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login endpoint called for user: {form_data.username}")
    return login_for_access_token(form_data.username, form_data.password, db)


@router.get("/verify-email", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def verify_email(request: Request, token: str = Query(...), db: Session = Depends(get_db)):
    logger.info(f"Email verification endpoint called with token: {token}")
    user = verify_user_email(token, db)
    return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Email verified successfully")


@router.post("/resend-verification", response_model=BaseResponse, status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def resend_verification(request: Request, email: EmailStr, db: Session = Depends(get_db)):
    logger.info(f"Resend verification endpoint called for email: {email}")
    resend_verification_email(email, db)
    return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="Verification email resent. Please check your email.")

