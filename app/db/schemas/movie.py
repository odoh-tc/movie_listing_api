from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class MovieBase(BaseModel):
    title: str
    description: str

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: UUID
    owner_id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class BaseResponse(BaseModel):
    success: bool
    status_code: int
    message: str
    data: Optional[Any] = None

    class Config:
        from_attributes = True
