from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User
from app.models.habit import Habit

# provide connection with mongoDB
async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)

    await init_beanie(
        database = client[settings.DATABASE_NAME],
        document_models = [User, Habit]
    )