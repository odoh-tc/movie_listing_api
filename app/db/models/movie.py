from sqlalchemy import Column, String, ForeignKey, Date, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.timestamp import Timestamp
import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import UniqueConstraint

class Movie(Base, Timestamp):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    poster_url = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    owner = relationship("User", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="movie", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('title', 'release_date', name='_title_release_date_uc'),)


