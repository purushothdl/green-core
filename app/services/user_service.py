from typing import Union
from app.repositories.user_repository import UserRepository
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.core.security import verify_password
from app.core.exceptions import InvalidCredentialsError, UserNotFoundError

class UserService:
    def __init__(self, users_collection):
        self.user_repo = UserRepository(users_collection)

    async def register_user(self, user: UserCreate) -> UserResponse:
        existing_user = await self.user_repo.get_user_by_email(user.email)
        if existing_user:
            raise InvalidCredentialsError("Email already registered")
        return await self.user_repo.create_user(user)

    async def authenticate_user(self, email: str, password: str) -> UserResponse:
        user = await self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user["password"]):
            raise InvalidCredentialsError("Invalid email or password")
        user["id"]=user["_id"]
        return UserResponse(**user)

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        user["id"]=user["_id"] 
        return UserResponse(**user)  
    
    async def update_user(self, user_id: str, update_data: Union[UserUpdate, dict]) -> UserResponse:
        if isinstance(update_data, UserUpdate):
            update_dict = update_data.dict(exclude_unset=True)
        else:
            update_dict = update_data

        if not update_dict:
            raise ValueError("No fields to update")
        updated_user = await self.user_repo.update_user(user_id, update_dict)
        updated_user["id"] = updated_user["_id"]  
        return UserResponse(**updated_user)
    