from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.timestamp import Timestamp
import uuid

class Rating(Base, Timestamp):
    __tablename__ = "ratings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    score = Column(Integer, nullable=False)
    review = Column(String, nullable=True)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
