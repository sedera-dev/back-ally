from fastapi import APIRouter, HTTPException, Depends
from app.modules.dify.models.chat_message import  UserMessage
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import json
import httpx

router = APIRouter()


@router.post("/chat-messages")
async def chat_with_dify(
    user_message: UserMessage,
    username: str = Depends(get_current_user)
    ):
    try:
        # En-têtes pour l'API Dify
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        
        payload = {
            "inputs": user_message.inputs,
            "query": user_message.query,
            "response_mode": user_message.response_mode,
            "conversation_id": user_message.conversation_id,
            "user": user_message.user
        }
        
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.DIFY_API_URL}/v1/chat-messages", json=payload, headers=headers)
       
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        try:
            # Tentative de conversion automatique
            return response.json()  
        except ValueError:
            try:
                # Tentative de conversion manuelle
                return json.loads(response.text)["data"] 
            except json.JSONDecodeError:
                return {"message": "Réponse en texte", "content": response.text} 
    except Exception as e:
        return { "Error": str(e)}
