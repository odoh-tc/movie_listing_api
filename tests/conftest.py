import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.models.user import Base
from app.db.session import get_db, engine

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
def reset_db():
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users"))
        conn.execute(text("DELETE FROM movies"))
        conn.execute(text("DELETE FROM comments"))
        conn.execute(text("DELETE FROM ratings"))
        conn.commit()
    yield

@pytest.fixture(scope="module")
def db():
    return TestingSessionLocal()
