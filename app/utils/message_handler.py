import logging

from typing import AsyncIterable, Dict

from .llm_manager import GeminiLLMManager
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager

    async def send_message_async(
            self, message: str,
            conversation_id: str,
            image: bool = False,
            image_url: str = None
    ) -> AsyncIterable[str]:
        try:

            # LLM configuration
            llm_manager = GeminiLLMManager()

            async for token in llm_manager.generate_async_response(message, conversation_id, image, image_url):
                yield token
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            raise

    async def flush_conversation_cache(self, project_id: str):
        # LLM configuration
        llm_manager = GeminiLLMManager()
        history = llm_manager.create_or_get_memory(project_id)
        history.clear()
        await self.cache_manager.flush_conversation_cache(project_id)

    async def save_conversation_config(self, project_id: str, config: Dict):
        await self.cache_manager.save_conversation_config(project_id, config)
