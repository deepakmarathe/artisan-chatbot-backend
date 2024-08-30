import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# from app.main import app
from app.models import User, Message

import app.schema as schemas
from app.crud import (
    get_user_by_username, create_user, authenticate_user,
    create_message, get_messages, get_message,
    update_message, delete_message
)

# Set up the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
from app.database import Base

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_user_by_username(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    user = create_user(db, schemas.UserCreate(username=username, password=password))
    fetched_user = get_user_by_username(db, username)
    assert fetched_user.username == user.username

