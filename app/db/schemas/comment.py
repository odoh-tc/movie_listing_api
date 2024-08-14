from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional, List
from datetime import datetime




class CommentSortOrder(str, Enum):
    MOST_RECENT = "most_recent"
    FROM_OLDEST = "from_oldest"

class CommentBase(BaseModel):
    content: str = Field(..., description="The content of the comment")
    movie_id: Optional[UUID] = Field(None, description="ID of the movie associated with the comment")

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: UUID = Field(..., description="Unique identifier for the comment")
    user_id: UUID = Field(..., description="Unique identifier for the user who made the comment")
    parent_comment_id: Optional[UUID] = Field(None, description="ID of the parent comment if this is a reply")
    created_at: datetime = Field(..., description="Timestamp when the comment was created")
    updated_at: datetime = Field(..., description="Timestamp when the comment was last updated")
    replies: Optional[List["CommentResponse"]] = Field(default=None, description="List of replies to this comment")

    model_config = ConfigDict(from_attributes=True, exclude_none=True)


CommentResponse.update_forward_refs()


class NestedCommentCreate(BaseModel):
    content: str = Field(..., description="The content of the nested comment")
    parent_comment_id: UUID = Field(..., description="ID of the parent comment")

class BaseResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the request was successful")
    status_code: int = Field(..., description="HTTP status code of the response")
    message: str = Field(..., description="Response message detailing the result")
    data: Optional[List[CommentResponse]] = Field(None, description="Response data containing comments")


    model_config = ConfigDict(from_attributes=True)

