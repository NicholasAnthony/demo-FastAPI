from passlib.context import CryptContext
from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from db import SessionLocal, init_db
from models_db import User, Token as TokenModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(username: str, password: str, email: str):
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            raise ValueError("User already exists")
        hashed = get_password_hash(password)
        user = User(username=username, hashed_password=hashed, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def authenticate_user(username: str, password: str):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    finally:
        db.close()


def create_access_token(username: str, expires_delta: timedelta = None) -> str:
    db: Session = SessionLocal()
    try:
        token = secrets.token_urlsafe(32)
        # store naive UTC datetime (SQLite doesn't preserve tzinfo reliably)
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
        token_model = TokenModel(token=token, username=username, expires=expire)
        db.add(token_model)
        db.commit()
        return token
    finally:
        db.close()


def get_current_user_from_token(token: str):
    db: Session = SessionLocal()
    try:
        data = db.query(TokenModel).filter(TokenModel.token == token).first()
        if not data:
            return None
        if data.expires < datetime.utcnow():
            db.delete(data)
            db.commit()
            return None
        user = db.query(User).filter(User.username == data.username).first()
        return user
    finally:
        db.close()


# Initialize DB schema on import (safe to call repeatedly)
init_db()
