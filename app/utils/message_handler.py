import logging

from typing import AsyncIterable

from .llm_manager import GeminiLLMManager

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, llm_manager: GeminiLLMManager):
        self.llm_manager = llm_manager

    async def send_message_async(
            self, message: str,
            conversation_id: str,
            image: bool = False,
            image_url: str = None
    ) -> AsyncIterable[str]:
        try:
            async for token in self.llm_manager.generate_async_response(message, conversation_id, image, image_url):
                yield token
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            raise

    async def flush_conversation_cache(self, project_id: str):
        # LLM configuration
        history = self.llm_manager.create_or_get_memory(project_id)
        history.clear()
