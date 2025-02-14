from fastapi import APIRouter, HTTPException, Depends
from app.modules.dify.models.chat_message import  ChatMessage
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import httpx

router = APIRouter()


@router.post("/{task_id}/stop")
async def stop_generate(
    task_id: str,
    user: str,
    username: str = Depends(get_current_user)
    ):
    try:
        # En-têtes pour l'API Dify
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "user": user
        }
       
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{settings.DIFY_API_URL}/chat-messages/{task_id}/stop", json=payload, headers=headers)
                response.raise_for_status()  # Lève une exception si le statut n'est pas 2xx
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Erreur lors de la communication avec l'API Dify: {e.response.text}",
                )

            # Renvoyer la réponse de l'API Dify
        return response.json()
        
       
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail= f"Error: {str(e)}"
        )
        
