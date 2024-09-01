from datetime import datetime, timedelta
from typing import List

import jwt
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .crud import (delete_message_crud, get_message_crud, update_message_crud, create_message_crud,
                  authenticate_user_crud, get_user_by_username_crud, create_user_crud, get_messages_crud)
from .database import Base
from .database import SessionLocal, engine

from .schemas import UserCreate, MessageCreate, MessageUpdate, Token, User, MessageServerResponse, Message

# Create the database tables
Base.metadata.create_all(bind=engine)

token_blacklist = set()

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:80", "http://52.71.98.179", "http://localhost"],  # Adjust the origin as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Authentication setup
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token in token_blacklist:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_username_crud(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username_crud(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user_crud(db=db, user=user)


@app.post("/register-form", response_model=User)
def register_user_form(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = get_user_by_username_crud(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = UserCreate(username=username, password=password)
    return create_user_crud(db=db, user=user)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user_crud(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username, "userid": user.id}


@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    token_blacklist.add(token)
    return {"msg": "Successfully logged out"}


# @app.post("/messages/", response_model=schemas.Message)
@app.post("/messages/", response_model=MessageServerResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    import time
    time.sleep(4)
    create_message_response = create_message_crud(db=db, message=message, user_id=current_user.id)

    # generate code to insert a new message record into the database, corresponding to the servers response
    server_message = MessageCreate(content="Server says: " + message.content)
    server_response = create_message_crud(db=db, message=server_message, user_id=current_user.id)

    res = {"message_create_response": create_message_response, "server_response": server_response}
    print(res)
    return res


@app.get("/messages/", response_model=List[Message])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    messages = get_messages_crud(db, user_id=current_user.id, skip=skip, limit=limit)

    # if not isinstance(messages, list):
    #     messages = list(messages)

    return messages


@app.put("/messages/{message_id}", response_model=Message)
def update_message(message_id: int, message: MessageUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_message = get_message_crud(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    if db_message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this message")
    return update_message_crud(db=db, message=message, message_id=message_id)


@app.delete("/messages/{message_id}", response_model=Message)
def delete_message(message_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    db_message = get_message_crud(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    if db_message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")
    return delete_message_crud(db=db, message_id=message_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
