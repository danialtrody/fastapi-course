# ============================================================
#                           IMPORTS
# ============================================================
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient
import pytest

from ..database import Base
from ..main import app
from ..models import ToDos, Users
from ..routers.auth import bcrypt_context


# ============================================================
#                    TEST DATABASE CONFIG
# ============================================================
SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


# ============================================================
#                    DEPENDENCY OVERRIDES
# ============================================================
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        "username": "danial",
        "id": 1,
        "user_role": "admin",
    }


# ============================================================
#                    TEST CLIENT
# ============================================================
client = TestClient(app)


# ============================================================
#                    FIXTURES – TODO
# ============================================================
@pytest.fixture()
def test_todo():
    todo = ToDos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield db

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


# ============================================================
#                    FIXTURES – USER
# ============================================================
@pytest.fixture()
def test_user():
    db = TestingSessionLocal()

    # Clean users table to avoid UNIQUE constraint issues
    db.execute(text("DELETE FROM users"))
    db.commit()

    user = Users(
        username="danialtest",
        email="danialtest@gmail.com",
        first_name="danialtest",
        last_name="danialtest",
        hashed_password=bcrypt_context.hash("123"),
        role="admin",
        phone_number="0545361151",
    )

    db.add(user)
    db.commit()

    yield user

    db.close()
