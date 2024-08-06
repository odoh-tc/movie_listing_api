from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    movie_id: Optional[UUID] = None

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: UUID
    user_id: UUID
    parent_comment_id: Optional[UUID] = None
    replies: List["CommentResponse"] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

CommentResponse.update_forward_refs()

class NestedCommentCreate(BaseModel):
    content: str
    parent_comment_id: UUID

class BaseResponse(BaseModel):
    success: bool
    status_code: int
    message: str
    data: Optional[List[CommentResponse]] = None

    class Config:
        from_attributes = True
