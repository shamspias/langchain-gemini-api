import logging

from typing import AsyncIterable, Dict

from .llm_manager import GeminiLLMManager
from .cache_manager import CacheManager

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager

    async def send_message_async(self, message: str, project_id: str, conversation_id: str) -> AsyncIterable[str]:
        try:

            # LLM configuration
            llm_manager = GeminiLLMManager()

            async for token in llm_manager.generate_async_response(message, conversation_id):
                yield token
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            raise

    async def flush_project_cache(self, project_id: str):
        await self.cache_manager.flush_conversation_cache(project_id)

    async def save_project_config(self, project_id: str, config: Dict):
        await self.cache_manager.save_conversation_config(project_id, config)
