# routes/chat_routes.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from app.services.chat_service import ChatService
from app.dependencies.service_dependencies import get_chat_service
from app.dependencies.auth_dependencies import get_current_user
from app.schemas.chat import ChatSession, ChatList

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/start", response_model=ChatSession)
async def start_chat(
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    image_data = await image.read() if image else None
    return await chat_service.start_chat(
        user_id=str(current_user.id),
        message=message,
        image=image_data,
    )

@router.post("/continue", response_model=ChatSession)
async def continue_chat(
    session_id: str = Form(...),
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    image_data = await image.read() if image else None
    return await chat_service.continue_chat(
        session_id=session_id,
        message=message,
        image=image_data,
    )

@router.delete("/end/{session_id}")
async def end_chat(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    await chat_service.end_chat(session_id)
    return {"message": "Chat session ended successfully"}

@router.get("/user", response_model=List[ChatList])
async def get_chats_by_user(
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.get_chats_by_user(str(current_user.id))