from fastapi import (
    HTTPException, 
    Response, 
    status
)
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone

from app.core.security import hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.token import TokenData
from app.utils.pagination import paginate

# create new user and add to database
async def create_user(user: UserCreate):
    # if user already exists by specific email
    if await User.find_one(User.email == user.email):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email exists"
        )
    
    # if user already exists by specific username 
    if await User.find_one(User.username == user.username):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "Username exists"
        )
    
    # else 
    try :
        new_user = User(
            *user.model_dump(exclude = {"password"}),
            password = await hash(user.password)
        )

        # add new user to the database
        return await new_user.insert()
    
    # exception by duplicate email or username
    except DuplicateKeyError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Data conflict: The provided credentials are already in use."
        )


# get all users from database by admin access
async def get_all_users(page: int = 1, limit: int = 10):
    
    
    skip, limit = paginate(page, limit)
    # get all users from database
    return await User.find_all().skip(skip).limit(limit).to_list()


# get user's information by email and owner access
async def get_user_by_email(email: str, current_user: TokenData) -> User:
    # get user from database 
    user = await User.find_one(
        User.email == email,
        User.id == current_user.id,
        User.status == "active"
    )

    # if user does not exist by specific email and id
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "User not found"
        )
    
    # return user information
    return user


# update user's information by email and owner access
async def update_user_by_email(data: UserUpdate, current_user: TokenData) -> User:
    # get user from database
    user = await User.find_one(
        User.email == data.email,
        User.id == current_user.id,
        User.status == "active"
    )

    # if user does not exist 
    if not user:
        return HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    # delete undefined or null values
    update_data = data.update_data.model_dump(
        exclude_unset = True, 
        exclude_none = True
    )
    
    # if password is updated thus hash updated password
    if "password" in update_data:
        update_data["password"] = await hash(update_data["password"])

    update_data["updated_at"] = datetime.now(timezone.utc)

    # add updated information to the database
    await user.update({ 
        "$set" : update_data
    })

    # get user by updated infromation
    return await User.get(user.id)


# delete user from database
async def delete_user_by_email(email: str, current_user: TokenData):
    # find the user from database
    user = await User.find_one(
        User.email == email,
        User.id == current_user.id,
        User.status == "active"
    )

    # if user does not exist
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User not found"
        )
    
    # change the user'status to deleted 
    await user.update({
        "$set": {
            "status": "deleted"
        }
    })

    return Response(status_code = status.HTTP_204_NO_CONTENT)