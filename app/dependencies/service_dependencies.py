from fastapi import Depends
from app.repositories.chat_repository import ChatRepository
from app.services.chat_service import ChatService
from app.services.org_service import OrgService
from app.services.user_service import UserService
from app.database.mongodb import Users, Orgs, Waste, Chats
from app.services.waste_service import WasteService

# Get ChatRepository
def get_chat_repository():
    return ChatRepository(Chats)

def get_user_service():
    return UserService(Users)

def get_org_service():
    return OrgService(Orgs)

def get_waste_service():
    return WasteService(Waste)

def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository)):
    return ChatService(chat_repository)
