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
from app.core.logging import logger

# Secret keys
ACCESS_SECRET_KEY = settings.ACCESS_SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY

ALGORITHM = settings.ALGORITHM

# Expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


async def create_access_token(data: Dict):
    to_encode = data.copy()
    
    # Calculate access token expiration
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    
    # Encode JWT access token in a threadpool
    return await run_in_threadpool(
        jwt.encode,
        to_encode,
        ACCESS_SECRET_KEY,
        ALGORITHM
    )


async def verify_access_token(token: str, credentials_exception):
    try:
        # Decode and verify JWT access token
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

    except JWTError as error:
        # exc_info=True includes the complete stack traceback in the logs
        logger.error(f"JWT-Access-Token Error: {error}", exc_info = True)
        raise credentials_exception
    
    except Exception as error:
        # Log unexpected internal server errors with full details
        logger.error(f"Unexpected Access Token Exception: {error}", exc_info = True)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )


async def create_refresh_token(data: Dict):
    to_encode = data.copy()
    
    # Calculate refresh token expiration
    expire = datetime.now(timezone.utc) + timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    # Encode JWT refresh token in a threadpool
    return await run_in_threadpool(
        jwt.encode,
        to_encode,
        REFRESH_SECRET_KEY,
        ALGORITHM
    )


async def verify_refresh_token(token: str):
    try:
        # Decode and verify JWT refresh token
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
    
    except JWTError as error:
        # Log expired or corrupted refresh tokens
        logger.error(f"JWT-Refresh-Token Error: {error}", exc_info = True)
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh token"
        )

    except Exception as error:
        # Log any other unexpected exception during refresh verification
        logger.error(f"Unexpected Refresh-Token Exception: {error}", exc_info = True)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )
