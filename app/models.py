from datetime import datetime

import dotenv

dotenv.load_dotenv()

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# from app.database import Base
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    messages = relationship("Message", back_populates="owner")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="messages")
