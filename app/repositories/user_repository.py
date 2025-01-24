from bson import ObjectId
from app.core.exceptions import UserNotFoundError
from app.core.security import hash_password
from app.schemas.users import UserCreate, UserResponse
from datetime import datetime

from app.utils.mongo_utils import convert_objectids_to_strings

class UserRepository:
    def __init__(self, users_collection):
        self.users_collection = users_collection

    async def create_user(self, user: UserCreate) -> UserResponse:
        user_dict = user.dict()
        user_dict["created_at"] = datetime.utcnow()
        user_dict["password"] = hash_password(user_dict["password"])  # Hash password
        result = await self.users_collection.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return UserResponse(**user_dict)

    async def get_user_by_email(self, email: str):
        user = await self.users_collection.find_one({"email": email})
        return convert_objectids_to_strings(user)

    async def get_user_by_id(self, user_id: str):
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        return convert_objectids_to_strings(user)
    
    async def update_user(self, user_id: str, update_data: dict) -> dict:
        user_oid = ObjectId(user_id)
        result = await self.users_collection.update_one(
            {"_id": user_oid},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise UserNotFoundError("User not found")
        updated_user = await self.users_collection.find_one({"_id": user_oid})
        return convert_objectids_to_strings(updated_user)