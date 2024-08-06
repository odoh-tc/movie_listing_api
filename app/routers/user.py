from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.schemas.user import UserResponse, BaseResponse
from app.services.auth import get_current_user
from app.db.session import get_db
from app.logger.logger import logger

router = APIRouter()

@router.get("/me", response_model=BaseResponse, status_code=status.HTTP_200_OK)
def get_current_user_details(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Fetching current user info for: {current_user.email}")
    user_response = UserResponse.from_orm(current_user)
    return BaseResponse(success=True, status_code=status.HTTP_200_OK, message="User data fetched successfully", data=user_response)
