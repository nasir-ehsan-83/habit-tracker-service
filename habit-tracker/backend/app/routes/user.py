from fastapi import APIRouter, Depends
from typing import List

from app.dependencies.current_user import get_current_user
from app.dependencies.roles import require_role
from app.models.user import User
from app.schemas.token import TokenData
from app.schemas.user import (
    UserCreate, 
    UserPrivateOut, 
    UserAdminOut, 
    UserUpdate
)
from app.services.user_service import (
    create_user, 
    get_all_users,
    get_user_by_email, 
    update_user_by_email, 
    delete_user_by_email
)

router = APIRouter(
    prefix = '/users',
    tags = ['User']
)

# create new user
@router.post('/', response_model = UserPrivateOut)
async def create_new_user(user_in: UserCreate) -> User:
    
    return await create_user(user_in)

# get all users's information by admin access
@router.get('/admin-only', response_model = List[UserAdminOut])
async def get_users(user = Depends(require_role("admin")), page: int = 1, limit: int = 10) -> List[User]:

    return await get_all_users(page, limit)

# get user's information by email and owner access
@router.get('/email', response_model = UserPrivateOut)
async def get_user_email(email: str, current_user: TokenData = Depends(get_current_user)) -> User:

    return await get_user_by_email(email, current_user)

# update user's information by email and owner acccess
@router.put('/email', response_model = UserPrivateOut)
async def update_user(user_data: UserUpdate, current_user: TokenData = Depends(get_current_user)) -> User :

    return await update_user_by_email(user_data, current_user)

# delete user's information by email and owner access
@router.delete('/email')
async def delete_user(email: str, current_user: TokenData = Depends(get_current_user)):

    return await delete_user_by_email(email, current_user)