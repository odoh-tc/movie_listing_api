from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base
from app.db.timestamp import Timestamp

class User(Base, Timestamp):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expiry = Column(DateTime, nullable=True)

    movies = relationship("Movie", back_populates="owner", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
