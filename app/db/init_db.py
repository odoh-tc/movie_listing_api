from sqlalchemy.orm import Session
from app.db.session import Base, engine

def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
