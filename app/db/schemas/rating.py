from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID

class RatingScore(IntEnum):
    one_star = 1
    two_stars = 2
    three_stars = 3
    four_stars = 4
    five_stars = 5

class RatingBase(BaseModel):
    score: RatingScore
    review: Optional[str] = None

class RatingCreate(RatingBase):
    movie_id: UUID

class RatingResponse(RatingBase):
    id: UUID
    user_id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class AggregatedRating(BaseModel):
    average_score: Optional[float] = None

class RatingsWithAggregation(BaseModel):
    ratings: list[RatingResponse]
    aggregated_rating: AggregatedRating

    class Config:
        from_attributes = True

class BaseResponse(BaseModel):
    success: bool
    status_code: int
    message: str
    data: Optional[Any] = None

    class Config:
        from_attributes = True
