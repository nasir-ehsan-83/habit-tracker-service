from typing import Dict
from fastapi import (
    HTTPException,
    Request,
    Response,
    status
)
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.core.security import verify
from app.core.oauth2 import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)


async def handle_login(response: Response, user_credential: OAuth2PasswordRequestForm ) -> Dict:
    # get user from database
    user = await User.find_one(User.username == user_credential.username)

    # if user not found
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )

    # if user found but is inactive or deleted
    if user.status != "active":
        raise HTTPException(
            staus_code = status.HTTP_403_FORBIDDEN,
            detail = "User account is inactive"
        )
    
    # verify password 
    if not await verify(user_credential.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )

    # create JWT access-token 
    access_token = await create_access_token({
        "id": str(user.id),
        "role": user.role
    })

    # create JWT refresh-token
    refresh_token = await create_refresh_token({
        "id": str(user.id),
        "role": user.role
    })

    # add refresh token to database
    await user.update({
        "$set": {
            "refresh_token": refresh_token
        }
    })

    # return refresh-token as cookie
    response.set_cookie(
        key = "jwt",
        value = refresh_token,
        httponly = True,
        max_age = 7 * 24 * 60 * 60
    )

    # return access-token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def handle_refresh_token(request: Request) -> Dict:
    # get refresh-token from cookies
    refresh_token = request.cookies.get("jwt")

    # if refresh-token not exists
    if not refresh_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Refresh token not found"
        )

    payload = await verify_refresh_token(refresh_token)

    # get user form database
    user = await User.get(payload["id"])

    # if user not found
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "User not found"
        )

    # if user is inactive or deleted
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # verify refresh-token with user.refresh_token
    if user.refresh_token != refresh_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh token"
        )

    # create new JWT access-token
    access_token = await create_access_token({
        "id": payload["id"],
        "role": payload["role"]
    })

    # retun new access-token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def handle_logout(request: Request):
    # get refresh-token from cookies
    refresh_token = request.cookies.get("jwt")

    response = Response(status_code = status.HTTP_204_NO_CONTENT)

    # if refresh-token not found
    if not refresh_token:
        response.delete_cookie("jwt")
        return response

    try:
        payload = await verify_refresh_token(refresh_token)
        # get user form datbase by id
        user = await User.get(payload["id"])
        
        # if user found 
        if user:
            await user.update({
                "$set": {
                    "refresh_token": None
                }
            })

    except Exception:
        pass

    response.delete_cookie("jwt")

    return response