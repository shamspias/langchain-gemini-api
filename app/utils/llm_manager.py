import logging
from typing import AsyncIterable

from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks import AsyncIteratorCallbackHandler

from ..config import settings

logger = logging.getLogger(__name__)


class GeminiLLMManager:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.redis_url = settings.REDIS_URL
        self.conversation_chain = None
        self.callback = AsyncIteratorCallbackHandler()

    def create_or_get_memory(self, conversation_id):
        message_history = RedisChatMessageHistory(url=settings.REDIS_URL, ttl=600, session_id=conversation_id)
        return ConversationBufferWindowMemory(memory_key="chat_history", chat_memory=message_history,
                                              return_messages=True,
                                              max_token_limit=4000)

    async def add_conversation_to_memory(self, conversation_id, user_message, ai_message):
        history = self.create_or_get_memory(conversation_id)
        history.save_context({"input": user_message}, {"output": ai_message})

    def get_gemini_model(self, image: bool = False):
        if image:
            model = ChatGoogleGenerativeAI(google_api_key=settings.GEMINI_API_KEY,
                                           stream=True,
                                           model="gemini-pro-vision",
                                           convert_system_message_to_human=True,
                                           callbacks=[self.callback],
                                           )
        else:
            model = ChatGoogleGenerativeAI(google_api_key=settings.GEMINI_API_KEY,
                                           stream=True,
                                           model="gemini-pro",
                                           convert_system_message_to_human=True,
                                           callbacks=[self.callback],
                                           )

        return model

    async def generate_async_response(self, message: str,
                                      conversation_id: str,
                                      image: bool = False,
                                      image_url: str = None
                                      ) -> AsyncIterable[str]:

        model = self.get_gemini_model(image)
        memory = self.create_or_get_memory(conversation_id=conversation_id)
        chat_memory = memory.load_memory_variables({})
        history = chat_memory["chat_history"]

        if not history:
            if image_url and image:
                message_list = [
                    SystemMessage(content=settings.SYSTEM_INSTRUCTION),
                    HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": message,
                            },  # You can optionally provide text parts
                            {"type": "image_url", "image_url": image_url},
                        ]
                    )
                ]
            else:
                message_list = [
                    SystemMessage(content=settings.SYSTEM_INSTRUCTION),
                    HumanMessage(content=message)
                ]

        else:
            if image_url and image:
                message_list = [SystemMessage(content=settings.SYSTEM_INSTRUCTION)] + history + [
                    HumanMessage(
                        content=[
                            {
                                "type": "text",
                                "text": message,
                            },  # You can optionally provide text parts
                            {"type": "image_url", "image_url": image_url},
                        ]
                    )
                ]
            else:
                message_list = [SystemMessage(content=settings.SYSTEM_INSTRUCTION)] + history + [
                    HumanMessage(content=message)]
        response = ""

        async for token in model.astream(input=message_list):
            response += f"{repr(token.content)}"
            yield f"{repr(token.content)}".encode("utf-8", errors="replace")

        await self.add_conversation_to_memory(conversation_id, message, response)
