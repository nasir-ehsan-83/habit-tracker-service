from datetime import (
    datetime,
    timezone,
    timedelta
)
from typing import Dict
from jose import jwt
from jose import JWTError
from fastapi import (
    HTTPException,
    status
)
from fastapi.concurrency import run_in_threadpool

from app.schemas.token import TokenData
from app.core.config import settings

# secret key
ACCESS_SECRET_KEY = settings.ACCESS_SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY

ALGORITHM = settings.ALGORITHM

# expire time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

async def create_access_token(data: Dict):

    to_encode = data.copy()

    # create expire minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    # create JWT access-token
    return await run_in_threadpool(
        jwt.encode,
        to_encode,
        ACCESS_SECRET_KEY,
        ALGORITHM
    )

async def verify_access_token(token: str,credentials_exception):
    
    try:
        # verify JWT token
        payload = await run_in_threadpool(
            jwt.decode,
            token,
            ACCESS_SECRET_KEY,
            [ALGORITHM]
        )

        if payload.get("type") != "access":
            raise credentials_exception

        id = payload.get("id")
        role = payload.get("role")

        if not id or not role:
            raise credentials_exception

        return TokenData(
            id = id,
            role = role
        )

    # jwt-exception
    except JWTError as error:
        raise credentials_exception
    
    except Exception as error:
        # unwanted exception
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )


async def create_refresh_token(data: Dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    # create JWT refresh-token
    return await run_in_threadpool(
        jwt.encode,
        to_encode,
        REFRESH_SECRET_KEY,
        ALGORITHM
    )

async def verify_refresh_token(token: str):

    try:
        # vreify refresh-token
        payload = await run_in_threadpool(
            jwt.decode,
            token,
            REFRESH_SECRET_KEY,
            [ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid refresh token"
            )

        return payload
    
    # jwt-excetion 
    except JWTError as error:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh token"
        )

    # other exceptoins
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )