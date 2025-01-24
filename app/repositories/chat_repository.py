# repositories/chat_repository.py
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from app.schemas.chat import ChatSession, ChatResponse, ChatList

class ChatRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def save_chat_session(self, chat_session: ChatSession):
        await self.collection.insert_one(chat_session.dict())

    async def get_chat_session(self, session_id: str) -> Optional[ChatResponse]:
        session_data = await self.collection.find_one({"session_id": session_id})
        return ChatResponse(**session_data) if session_data else None

    async def update_chat_session(self, chat_session: ChatSession):
        await self.collection.update_one(
            {"session_id": chat_session.session_id},
            {"$set": chat_session.dict()},
        )

    async def delete_chat_session(self, session_id: str):
        await self.collection.delete_one({"session_id": session_id})

    async def get_chats_by_user(self, user_id: str) -> List[ChatList]:
        cursor = self.collection.find({"user_id": user_id})
        chat_list = []
        async for chat_data in cursor:
            chat_list.append(ChatList(**chat_data))
        return chat_list