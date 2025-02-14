from fastapi import APIRouter, HTTPException, Depends
from app.modules.dify.models.message_feedback import  MessageFeedBack
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import json
import httpx

router = APIRouter()


@router.post("/{message_id}/feedbacks")
async def message_feedback(
    message_id: str,
    message: MessageFeedBack,
    username: str = Depends(get_current_user)
    ):
    try:
        # En-têtes pour l'API Dify
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "rating": message.rating,
            "user": message.user ,
            "content":   message.content
        }
       
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{settings.DIFY_API_URL}/messages/{message_id}/feedbacks", json=payload, headers=headers)
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
        
