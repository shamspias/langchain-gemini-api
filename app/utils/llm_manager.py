import asyncio
import logging
from typing import Awaitable

from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

from ..config import settings

logger = logging.getLogger(__name__)


class GeminiLLMManager:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.redis_url = settings.REDIS_URL
        self.conversation_chain = None

    def create_or_get_memory(self, conversation_id):
        message_history = RedisChatMessageHistory(url=settings.REDIS_MEMORY_URL, ttl=600, session_id=conversation_id)
        return ConversationBufferMemory(memory_key="chat_history", chat_memory=message_history, return_messages=True)

    async def add_conversation_to_memory(self, conversation_id, user_message, ai_message):
        history = self.create_or_get_memory(conversation_id)
        history.save_context({"input": user_message}, {"output": ai_message})

    async def get_gemini_pro_text_model(self):
        model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
        model(
            [
                SystemMessage(content=settings.SYSTEM_INSTRUCTION),
            ]
        )
        return model

    async def get_gemini_pro_vision_model(self):
        llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", convert_system_message_to_human=True)
        llm(
            [
                SystemMessage(content=settings.SYSTEM_INSTRUCTION),
            ]
        )

        return llm

    async def generate_async_response(self, message: str, conversation_id: str, image: bool = False,
                                      image_url: str = None):
        if image:
            model = await self.get_gemini_pro_vision_model()
        else:
            model = await self.get_gemini_pro_text_model()

        response = ""
        async for chunk in model.astream(message):
            response += chunk.content
            yield chunk.content
        await self.add_conversation_to_memory(conversation_id, message, response)
