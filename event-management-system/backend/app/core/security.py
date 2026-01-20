from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from jose import JWTError
from pydantic import BaseModel
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from authlib.integrations.starlette_client import OAuth

SECRET_KEY = "31a4203acf14f91f2ec26dd39eafcc4e79bd7720207ee728c091d39aa966ebcd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token : str
    token_type : str
    user: dict | None = None

def get_password_hash(password: str):
    """Hash a password using bcrypt"""
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    """Verify a password against a bcrypt hash"""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def create_access_token(data: dict , expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.JWTError:
        return None

#google facebook login auth

oauth = OAuth()

oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid profile email'},
)

oauth.register(
    name='facebook',
    client_id='your-facebook-client-id',
    client_secret='your-facebook-client-secret',
    authorize_url='https://www.facebook.com/v9.0/dialog/oauth',
    authorize_params=None,
    access_token_url='https://graph.facebook.com/v9.0/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'email'},
)



