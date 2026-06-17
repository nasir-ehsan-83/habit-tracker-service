from typing import (
    List, 
    Optional
)
from fastapi import (
    APIRouter, 
    Depends
)
from app.models.habit import Habit
from app.dependencies.current_user import get_current_user
from app.dependencies.roles import require_role
from schemas.token import TokenData
from app.utils.limiter import limiter
from app.schemas.habit import (
    HabitCreate, 
    HabitPrivateOut, 
    HabitAdminOut, 
    HabitUpdate
)
from app.services.habit_service import(
    create_new_habit,
    get_all_habits_owner,
    get_all_habits_admin, 
    get_habit_by_name,
    update_habit_by_name,
    delete_habit_by_name
)


router = APIRouter(
    prefix = '/habits',
    tags = ["Habits"]
)


@router.post('/', response_model = HabitPrivateOut)
@limiter.limit('3/minute')
async def create_habit(habit: HabitCreate, current_user: TokenData = Depends(get_current_user)) -> Habit:
    
    return await create_new_habit(habit, current_user)


# get all habits of specific user by  owner access
@router.get('/', response_model = List[HabitAdminOut])
async def get_habits_owner(current_user: TokenData = Depends(get_current_user), page: int = 1, limit: int = 10) -> List[Habit]:
    
    return await get_all_habits_owner(current_user, page, limit)


# get all habits of all usres by admin access
@router.get('/only-admin', response_model = List[HabitPrivateOut])
async def get_habits_admin(owner_id: Optional[int] = None, page: int = 1, limit: int = 10, user = Depends(require_role(2020))) -> List[Habit]:
    
    return await get_all_habits_admin(owner_id, page, limit)


@router.get('/name', response_model = HabitPrivateOut)
async def get_habit(name: str, current_user: TokenData = Depends(get_current_user)) -> Habit:

    return await get_habit_by_name(name, current_user)


@router.put('/name', response_model = HabitPrivateOut)
async def update_habit(name: str, update_habit: HabitUpdate, current_user: TokenData = Depends(get_current_user)) -> Habit:
    
    return await update_habit_by_name(name, update_habit, current_user)


@router.delete('/name')
async def delete_habit(name: str, current_user: TokenData = Depends(get_current_user)) :

    return await delete_habit_by_name(name, current_user)