from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    userid: int

class TokenData(BaseModel):
    username: Optional[str] = None
