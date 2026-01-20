from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password, Token, ACCESS_TOKEN_EXPIRE_MINUTES, oauth
from app.core.database import get_db
from app.crud.user_crud import get_user_by_email, create_user
from app.schemas.user_schema import UserCreate
from starlette.requests import Request

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "profile_image": user.profile_image
        }
    }

# Google OAuth
@router.get("/auth/google/login")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google", name="auth_google_callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if not user:
         user = await oauth.google.parse_id_token(request, token)
    return {"user": user}

# Facebook OAuth
@router.get("/auth/facebook/login")
async def login_facebook(request: Request):
    redirect_uri = request.url_for('auth_facebook_callback')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get("/auth/facebook", name="auth_facebook_callback")
async def auth_facebook_callback(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    user = await oauth.facebook.parse_id_token(request, token)
    return {"user": user}