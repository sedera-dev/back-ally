from fastapi import APIRouter
from app.modules.dify.api.v1.endpoints import chat_message, files_upload, message_feedbacks, stop_generate, next_suggested_questions, get_conversation_history_messages

router = APIRouter()

router.include_router(chat_message.router, prefix="/chat-messages")
router.include_router(files_upload.router, prefix="/files/upload")
router.include_router(stop_generate.router, prefix="/chat-messages")
router.include_router(message_feedbacks.router, prefix="/messages")
router.include_router(next_suggested_questions.router, prefix="/messages")
router.include_router(get_conversation_history_messages.router, prefix="/messages")