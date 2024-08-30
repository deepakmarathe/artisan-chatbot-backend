import uuid

from dotenv import load_dotenv
load_dotenv()

import pytest
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chatbot.schemas import UserCreate, MessageCreate, MessageUpdate

from chatbot.crud import (
    get_user_by_username_crud, create_user_crud, authenticate_user_crud,
    create_message_crud, get_messages_crud, get_message_crud,
    update_message_crud, delete_message_crud
)

# from app.main import app

# Set up the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
from chatbot.database import Base

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
    user = create_user_crud(db, UserCreate(username=username, password=password))
    fetched_user = get_user_by_username_crud(db, username)
    assert fetched_user.username == user.username


def test_create_user(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    assert user.username == username
    assert pwd_context.verify(password, user.hashed_password)


def test_authenticate_user(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    authenticated_user = authenticate_user_crud(db, username, password)
    assert authenticated_user
    assert authenticated_user.username == username


def test_create_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    message = create_message_crud(db, MessageCreate(content="Hello, World!"), user.id)
    assert message
    assert message.id
    assert message.content == "Hello, World!"
    assert message.user_id == user.id


def test_get_messages(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    create_message_crud(db, MessageCreate(content="Message 1"), user.id)
    create_message_crud(db, MessageCreate(content="Message 2"), user.id)
    messages = get_messages_crud(db, user.id)
    assert messages
    assert len(list(messages)) == 2
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Message 2"


def test_get_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    message = create_message_crud(db, MessageCreate(content="Single Message"), user.id)
    fetched_message = get_message_crud(db, message.id)
    assert fetched_message
    assert fetched_message.content == "Single Message"


def test_update_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    message = create_message_crud(db, MessageCreate(content="Old Content"), user.id)
    updated_message = update_message_crud(db, MessageUpdate(content="New Content"), message.id)
    assert updated_message.content == "New Content"


def test_delete_message(db):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())

    user = create_user_crud(db, UserCreate(username=username, password=password))
    message = create_message_crud(db, MessageCreate(content="To be deleted"), user.id)
    delete_message_crud(db, message.id)
    fetched_message = get_message_crud(db, message.id)
    assert fetched_message is None
