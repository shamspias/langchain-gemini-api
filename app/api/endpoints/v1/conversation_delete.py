from fastapi import APIRouter, HTTPException, Depends
from app.utils.message_handler import MessageHandler
from app.utils.cache_manager import CacheManager

from app.permissions import verify_api_key
from app.config import settings

router = APIRouter()


@router.delete("/{conversation_id}")
async def config_update(conversation_id: str, api_key: str = Depends(verify_api_key)):
    cache_manager = CacheManager(settings.REDIS_URL)
    message_handler = MessageHandler(cache_manager)

    try:
        await message_handler.flush_conversation_cache(conversation_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
