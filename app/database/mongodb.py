from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client.get_database(settings.DATABASE_NAME)

Users = db.users
Orgs = db.orgs
Waste = db.waste
Chats = db.chats