from datetime import datetime, timezone
from typing import Optional
from pydantic import EmailStr, Field
from pymongo import IndexModel, ASCENDING
from beanie import Document

from app.utils.enum import UserRole, UserStatus

class User(Document):
    name: str
    username: str
    email: EmailStr  
    password: str

    role: UserRole = UserRole.user
    status: UserStatus = UserStatus.active
    
    created_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory = lambda: datetime.now(timezone.utc))

    refresh_token: Optional[str]
    
    class Settings:
        name = "users"
        # Correct way to define unique indexes in Beanie Settings
        indexes = [
            IndexModel([("email", ASCENDING)], unique = True),
            IndexModel([("username", ASCENDING)], unique = True),
        ]
