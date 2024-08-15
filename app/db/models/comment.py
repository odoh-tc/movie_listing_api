from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.session import Base
from app.db.timestamp import Timestamp

class Comment(Base, Timestamp):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(String(1000), index=True)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id"), nullable=True)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="comments")
    movie = relationship("Movie", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent_comment", cascade="all, delete-orphan", lazy="selectin")


    