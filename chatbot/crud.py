from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .models import User, Message
from .schemas import UserCreate, MessageCreate, MessageUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username_crud(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user_crud(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user_crud(db: Session, username: str, password: str):
    user = get_user_by_username_crud(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_message_crud(db: Session, message: MessageCreate, user_id: int):
    db_message = Message(**message.dict(), user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_crud(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Message).filter(Message.user_id == user_id).offset(skip).limit(limit)


def get_message_crud(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


def update_message_crud(db: Session, message: MessageUpdate, message_id: int):
    db_message = get_message_crud(db, message_id)
    if db_message:
        db_message.content = message.content
        db.commit()
        db.refresh(db_message)
    return db_message


def delete_message_crud(db: Session, message_id: int):
    db_message = get_message_crud(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message
