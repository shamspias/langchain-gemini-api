from pydantic import BaseModel
from typing import Optional, Text


class ChatRequest(BaseModel):
    message_id: Optional[str] = None
    query: str
    conversation_id: Optional[str]


class ChatResponse(BaseModel):
    response: Text
