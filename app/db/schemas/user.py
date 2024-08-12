from datetime import datetime
import re
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    first_name: str = Field(..., description="The user's first name")
    last_name: str = Field(..., description="The user's last name")


class UserCreate(UserBase):
    password: str = Field(..., description="The user's password")

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least one number')
        return v

class UserResponse(UserBase):
    id: UUID = Field(..., description="Unique identifier for the user")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the user was created")
    is_verified: bool = Field(..., description="Indicates whether the user's email is verified")


    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of the token, usually 'bearer'")


class BaseResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the request was successful")
    status_code: int = Field(..., description="HTTP status code of the response")
    message: str = Field(..., description="Response message detailing the result")
    data: Optional[Any] = Field(None, description="Response data containing user information or related data")

    model_config = ConfigDict(from_attributes=True)


class EmailVerification(BaseModel):
    token: str = Field(..., description="The email verification token")