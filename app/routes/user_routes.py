from typing import Dict
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserCreate, UserResponse, Token, UserUpdate
from app.services.user_service import UserService
from app.dependencies.service_dependencies import get_user_service
from app.core.security import create_access_token
from app.dependencies.auth_dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.register_user(user)

@router.post("/login", response_model=Token)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(email, password)
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_details(
    current_user: UserResponse = Depends(get_current_user),
):  
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user(
    update_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user),
):
    return await user_service.update_user(current_user.id, update_data)