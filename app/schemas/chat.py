# schemas/chat.py
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ChatMessage(BaseModel):
    sender: str  # "user" or "bot"
    text: str
    timestamp: datetime

class ChatSession(BaseModel):
    session_id: str
    user_id: str
    messages: List[ChatMessage] = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class ChatResponse(BaseModel):
    session_id: str
    user_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime

class ChatList(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime