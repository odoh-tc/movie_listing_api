from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any
from uuid import UUID

class RatingScore(IntEnum):
    one_star = 1
    two_stars = 2
    three_stars = 3
    four_stars = 4
    five_stars = 5

class RatingBase(BaseModel):
    score: RatingScore = Field(..., description="The rating score, from 1 to 5")
    review: Optional[str] = Field(None, description="Optional review text accompanying the rating")

class RatingCreate(RatingBase):
    movie_id: UUID = Field(..., description="ID of the movie being rated")

class RatingResponse(RatingBase):
    id: UUID = Field(..., description="Unique identifier for the rating")
    user_id: UUID = Field(..., description="Unique identifier for the user who gave the rating")
    created_at: Optional[datetime] = Field(None, description="Timestamp when the rating was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the rating was last updated")

    model_config = ConfigDict(from_attributes=True)


class AggregatedRating(BaseModel):
    average_score: Optional[float] = Field(None, description="The average rating score for the movie")

class RatingsWithAggregation(BaseModel):
    ratings: list[RatingResponse] = Field(..., description="List of individual ratings for the movie")
    aggregated_rating: AggregatedRating = Field(..., description="Aggregated rating information")

    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the request was successful")
    status_code: int = Field(..., description="HTTP status code of the response")
    message: str = Field(..., description="Response message detailing the result")
    data: Optional[Any] = Field(None, description="Response data containing ratings or related information")

    model_config = ConfigDict(from_attributes=True)

