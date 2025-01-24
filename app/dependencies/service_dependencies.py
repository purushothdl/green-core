from app.services.user_service import UserService
from app.database.mongodb import Users

# Dependency to inject UserService
def get_user_service():
    return UserService(Users)