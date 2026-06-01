from fastapi.concurrency import run_in_threadpool
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from typing import Dict

from app.schemas.token import TokenData
from app.core.confing import settings


ACCESS_SECRET_KEY = settings.ACCESS_SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY

ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

async def create_access_token(data: Dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "access"  
    })

    return  await run_in_threadpool(
        jwt.encode,
        to_encode,
        ACCESS_SECRET_KEY,
        algorithm = ALGORITHM
    )


async def verify_access_token(token: str, credentials_exception: str):
    try:
        payload = await run_in_threadpool(
            jwt.decode,
            token,
            ACCESS_SECRET_KEY,
            algorithms = [ALGORITHM]
        )

        if payload.get("type") != "access":
            raise credentials_exception
        
        id: str = payload.get("user_id")
        role: str = payload.get("role")

        if id is None or role is None:
            raise credentials_exception
        
        return TokenData(id = str(id), role = role)

    except JWTError:
        raise credentials_exception
    
async def create_refresh_token(data: Dict): 
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return await run_in_threadpool(
        jwt.encode,
        to_encode,
        REFRESH_SECRET_KEY,
        algorithm = ALGORITHM
    )

async def verify_refresh_token(token: str, credentials_exception: str):

    try:
        payload = await run_in_threadpool(
            jwt.decode,
            token,
            REFRESH_SECRET_KEY,
            algorithm = [ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise credentials_exception
        
        return payload
    
    except JWTError:
        raise credentials_exception