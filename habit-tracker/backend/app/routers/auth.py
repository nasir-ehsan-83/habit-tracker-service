from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.token import Token
from app.services.auth_service import login

router = APIRouter(
    tabs = ["Authentication"]
)

@router.post('/login', response_model = Token)
async def user_login(user_credential: Annotated[OAuth2PasswordRequestForm, Depends()]):

    return await login(user_credential)

@router.post('/refresh')
async def refresh(token: str):
    
    return await refresh_access_token(token)