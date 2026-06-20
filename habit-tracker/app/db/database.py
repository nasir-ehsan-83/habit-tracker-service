from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User
from app.models.habit import Habit
from app.core.logging import logger 

# Provide connection with MongoDB
async def init_db():
    try:
        client = AsyncIOMotorClient(settings.MONGO_URL)

        await init_beanie(
            database = client[settings.DATABASE_NAME],
            document_models = [User, Habit]
        )
    except Exception as error:
        logger.critical(f"Database Initialization Failed: {error}", exc_info = True)
        raise error
