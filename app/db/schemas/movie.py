from enum import Enum
from typing import Any, Optional
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, validator
from datetime import datetime, date
from uuid import UUID


class SortByEnum(str, Enum):
    most_rated = "most_rated"
    most_recent = "most_recent"
    most_rated_and_recent = "most_rated_and_recent"

class MovieBase(BaseModel):
    title: str = Field(..., description="The title of the movie")
    description: str = Field(..., description="A brief description of the movie")
    duration: int = Field(..., description="Duration of the movie in minutes")
    release_date: date = Field(..., description="The release date of the movie")
    poster_url: Optional[AnyUrl] = Field(None, description="URL to the movie's poster image")

    @validator('duration')
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError('Duration must be greater than zero')
        return v

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    description: Optional[str] = Field(None, description="A brief description of the movie")
    poster_url: Optional[AnyUrl] = Field(None, description="URL to the movie's poster image")


class MovieResponse(MovieBase):
    id: UUID = Field(..., description="Unique identifier for the movie")
    owner_id: UUID = Field(..., description="Unique identifier for the user who added the movie")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the movie was added")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the movie was last updated")

    model_config = ConfigDict(from_attributes=True)

class BaseResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the request was successful")
    status_code: int = Field(..., description="HTTP status code of the response")
    message: str = Field(..., description="Response message detailing the result")
    data: Optional[Any] = Field(None, description="Response data containing movies or related information")

    model_config = ConfigDict(from_attributes=True)

