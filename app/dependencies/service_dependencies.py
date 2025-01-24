from app.services.org_service import OrgService
from app.services.user_service import UserService
from app.database.mongodb import Users, Orgs, Waste, Chats
from app.services.waste_service import WasteService

def get_user_service():
    return UserService(Users)

def get_org_service():
    return OrgService(Orgs)

def get_waste_service():
    return WasteService(Waste)

def get_chat_service():
    return ChatService(Chats)