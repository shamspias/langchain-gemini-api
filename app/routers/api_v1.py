from fastapi import APIRouter
from app.api.endpoints.v1 import conversation, conversation_delete

api_router = APIRouter()

api_router.include_router(conversation.router, prefix="/api/v1/conversations", tags=["conversation"])

api_router.include_router(conversation_delete.router, prefix="/api/v1/delete", tags=["conversation-delete"])
