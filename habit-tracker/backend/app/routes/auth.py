from fastapi import (
    APIRouter, 
    Depends, 
    Request, 
    Response
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated

from app.schemas.token import Token
from app.services.auth_service import (
    handle_login, 
    handle_refresh_token, 
    handle_logout
)

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login', response_model = Token)
async def login(response: Response, user_credential: Annotated[OAuth2PasswordRequestForm, Depends()]):

    return await handle_login(response, user_credential)

@router.get('/refresh', response_model = Token)
async def refresh(request: Request):
    return await handle_refresh_token(request)

@router.get('/logout')
async def logout(request: Request):
    return await handle_logout(request)