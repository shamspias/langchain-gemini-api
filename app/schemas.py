from pydantic import BaseModel
from typing import Optional, Text


class ChatRequest(BaseModel):
    message_id: Optional[str] = None
    query: str
    conversation_id: Optional[str]
    image: bool = Optional[False]
    image_url: Optional[str] = None


class ChatResponse(BaseModel):
    response: Text
