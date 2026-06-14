from typing import List, Optional
from fastapi import (
    HTTPException, 
    Response, 
    status
)
from pymongo.errors import DuplicateKeyError
from datetime import (
    datetime, 
    timezone
)
from app.models.habit import Habit
from app.schemas.habit import (
    HabitCreate, 
    HabitUpdate
)
from app.schemas.token import TokenData
from app.utils.pagination import paginate




async def create_new_habit(habit_in: HabitCreate, current_user: TokenData) -> Habit:
    
    # get habit from database by specific owner
    existing_habit = await Habit.find_one(
        Habit.name == habit_in.name,
        Habit.owner_id == current_user.id,
        Habit.status != "deleted"
    )
    
    # if user already has habit
    if existing_habit:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Habit already exists"
        )

    try:
        new_habit = Habit(
            **habit_in.model_dump(),
            owner_id = current_user.id
        )

        return await new_habit.insert()

    except DuplicateKeyError:
       
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Conflict: A habit with this name already exists for this user."
        )


async def get_all_habits_owner(current_user: TokenData, page: int = 1, limit: int = 10) -> List[Habit]:
    # calculate skip and limit values
    skip, limit = paginate(page, limit)
    
    # get all habits of users
    return  await Habit.find_all(
        Habit.owner_id == current_user.id, 
        Habit.status != "deleted"
    ).skip(skip).limit(limit).to_list()


async def get_all_habits_admin(owner_id: Optional[int] = None, page: int = 1, limit: int = 10) -> List[Habit]:
    
    # calculate skip and limit values
    skip, limit = paginate(page, limit)
    
    if owner_id is not None:
        return await Habit.find_all(
            Habit.owner_id == owner_id
        ).skip(skip).limit(limit).to_list()

    # else get all habits of all users 
    return await Habit.find_all().skip(skip).limit(limit).to_list()


async def get_habit_by_name(name: str, current_user: TokenData) -> Habit:
    # get habit by specific owner
    existing_habit = await Habit.find_one(
        Habit.name == name,
        Habit.owner_id == current_user.id,
        Habit.status != "deleted"   
    )

    # if habit does not exist
    if not existing_habit:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Habit not found"
        )
    
    # if habit exists then return 
    return existing_habit

async def update_habit_by_name(name: str, update_habit: HabitUpdate, current_user: TokenData) -> Habit:
    # get specific habit form database
    existing_habit = await Habit.find_one(
        Habit.name == name,
        Habit.owner_id == current_user.id,
        Habit.status != "deleted"
    )

    # if habit does not exist
    if not existing_habit:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Habit not found"
        )
    
    # delete undefined or null values
    update_data = update_habit.model_dump(
        exclude_unset = True, 
        exclude_none = True
    )

    update_data.update({
        "updated_at": datetime.now(timezone.utc)
    })
    
    # update habit and  store in database
    await existing_habit.update({
        "$set": update_data
    })
    
    # sync local object fields with database changes
    await existing_habit.sync()
    
    return existing_habit
    

async def delete_habit_by_name(name: str, current_user: TokenData):
    # get specific habit from database
    existing_habit = await Habit.find_one(
        Habit.name == name,
        Habit.owner_id == current_user.id,
        Habit.status != "deleted"
    )
    
    # if specific habit does not exist
    if not existing_habit:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Habit not found"
        )
    
    # if exists delete
    await existing_habit.update({
        "$set": {
            "status": "deleted"
        }
    })

    # return nothing
    return Response(status_code = status.HTTP_204_NO_CONTENT)
