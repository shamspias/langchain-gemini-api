from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest
from app.utils.message_handler import MessageHandler
from app.utils.cache_manager import CacheManager

from app.permissions import verify_api_key
from app.config import settings

router = APIRouter()

cache_manager = CacheManager(settings.REDIS_URL)
message_handler = MessageHandler(cache_manager)


@router.post("/{conversation_id}")
async def chat_with_model(conversation_id: str, chat_request: ChatRequest, api_key: str = Depends(verify_api_key)):
    try:
        message = chat_request.query
        image = chat_request.image
        image_url = chat_request.image_url
        return StreamingResponse(message_handler.send_message_async(message, conversation_id, image, image_url),
                                 media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
