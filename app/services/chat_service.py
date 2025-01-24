# services/chat_service.py
from datetime import datetime
from io import BytesIO
from typing import List, Optional
import uuid
import PIL
import google.generativeai as genai
from fastapi import HTTPException
from app.core.config import settings
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatList, ChatSession, ChatMessage

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    async def start_chat(
        self,
        user_id: str,
        message: Optional[str] = None,
        image: Optional[bytes] = None,
    ) -> ChatSession:
        
        chat = model.start_chat()
        input_content = []

        if message:
            input_content.append(f"User Query: {message}")
        if image:
            input_content.append(image)

        # Input prompt
        input_content.append(
            "You are a waste disposal assistant. Provide advice on how to dispose of the waste properly. "
            "If an image is provided, classify the waste and suggest the appropriate disposal method. "
            "Keep responses concise and informative."
        )

        response = chat.send_message(input_content)

        chat_session = ChatSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            messages=[
                ChatMessage(sender="user", text=message or "Started chat", timestamp=datetime.utcnow()),
                ChatMessage(sender="bot", text=response.text, timestamp=datetime.utcnow()),
            ],
        )

        await self.chat_repository.save_chat_session(chat_session)
        return chat_session

    async def continue_chat(
        self,
        session_id: str,
        message: str,
        image: Optional[bytes] = None,
    ) -> ChatSession:
        chat_session = await self.chat_repository.get_chat_session(session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Session not found")

        history = []
        for msg in chat_session.messages:
            if msg.sender == "user":
                history.append({"role": "user", "parts": [msg.text]})
            elif msg.sender == "bot":
                history.append({"role": "model", "parts": [msg.text]})

        chat = model.start_chat(history=history)
        input_content = [message]
        if image:
            img = await self._process_image(image)
            if img:
                input_content.append(img)

        # Input prompt
        input_content.append(
            "You are a waste disposal assistant. Provide advice on how to dispose of the waste properly. "
            "If an image is provided, classify the waste and suggest the appropriate disposal method. "
            "Keep responses concise and informative."
        )

        response = chat.send_message(input_content)

        chat_session.messages.extend([
            ChatMessage(sender="user", text=message, timestamp=datetime.utcnow()),
            ChatMessage(sender="bot", text=response.text, timestamp=datetime.utcnow()),
        ])
        chat_session.updated_at = datetime.utcnow()

        await self.chat_repository.update_chat_session(chat_session)
        return chat_session

    async def end_chat(self, session_id: str):
        chat_session = await self.chat_repository.get_chat_session(session_id)
        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        await self.chat_repository.delete_chat_session(session_id)

    async def get_chats_by_user(self, user_id: str) -> List[ChatList]:
        return await self.chat_repository.get_chats_by_user(user_id)
    
    async def _process_image(self, image: Optional[bytes]) -> Optional[PIL.Image.Image]:
        """
        Process an image from bytes.
        """
        if not image:
            return None

        try:
            img = PIL.Image.open(BytesIO(image))
            return img
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None