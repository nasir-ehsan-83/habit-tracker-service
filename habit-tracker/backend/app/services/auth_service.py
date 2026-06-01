from typing import Dict, Optional
from fastapi import HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm 

from app.models.user import User
from app.core.security import verify
from app.core.oauth2 import create_access_token, create_refresh_token, verify_refresh_token

async def login(user_credential: OAuth2PasswordRequestForm) -> Optional[Dict]:
    # get user from database
    user = await User.find_one(User.username == user_credential.username)

    # if specific user does not exist
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid credential"
        )

    # else verify password

    if not await verify(user_credential.password, user.password):
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Invalid credential"
        )

    # create acsess token
    access_token = await create_access_token(data = {
        "user_id": str(user.id),
        "role": user.role
    })

    # create refresh token
    refresh_token = await create_refresh_token(data = {
        "user_id" : str(user.id)
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_access_token(refresh_token: str) -> Optional[Dict]:

    payload = verify_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh token"
        )
    
    new_access_token = create_access_token(
        data = {
            "user_id": payload["user_id"],
            "user_role": payload["user_role"]
        }
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }