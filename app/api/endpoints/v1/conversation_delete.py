from fastapi import APIRouter, HTTPException, Depends, Header, Response
from app.utils.message_handler import MessageHandler
from app.utils.llm_manager import GeminiLLMManager

from app.permissions import verify_api_key
from app.config import settings

router = APIRouter()


@router.delete("/{conversation_id}")
async def config_update(conversation_id: str,
                        api_key: str = Depends(verify_api_key),
                        x_api_key: str = Header(None, alias='x-api-key')
                        ):
    llm_manager = GeminiLLMManager()
    message_handler = MessageHandler(llm_manager)

    try:
        await message_handler.flush_conversation_cache(conversation_id)
        return Response(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
