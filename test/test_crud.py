import uuid

import pytest
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.schema as schemas
from app.crud import (
    get_user_by_username, create_user, authenticate_user,
    create_message, get_messages, get_message,
    update_message, delete_message
)

# from app.main import app

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


def test_create_user(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    assert user.username == username
    assert pwd_context.verify(password, user.hashed_password)


def test_authenticate_user(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    authenticated_user = authenticate_user(db, username, password)
    assert authenticated_user
    assert authenticated_user.username == username


def test_create_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    message = create_message(db, schemas.MessageCreate(content="Hello, World!"), user.id)
    assert message
    assert message.id
    assert message.content == "Hello, World!"
    assert message.user_id == user.id


def test_get_messages(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    create_message(db, schemas.MessageCreate(content="Message 1"), user.id)
    create_message(db, schemas.MessageCreate(content="Message 2"), user.id)
    messages = get_messages(db, user.id)
    assert messages
    assert len(list(messages)) == 2
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Message 2"


def test_get_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    message = create_message(db, schemas.MessageCreate(content="Single Message"), user.id)
    fetched_message = get_message(db, message.id)
    assert fetched_message
    assert fetched_message.content == "Single Message"


def test_update_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    message = create_message(db, schemas.MessageCreate(content="Old Content"), user.id)
    updated_message = update_message(db, schemas.MessageUpdate(content="New Content"), message.id)
    assert updated_message.content == "New Content"


def test_delete_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user(db, schemas.UserCreate(username=username, password=password))
    message = create_message(db, schemas.MessageCreate(content="To be deleted"), user.id)
    delete_message(db, message.id)
    fetched_message = get_message(db, message.id)
    assert fetched_message is None
