from fastapi import APIRouter, HTTPException, Depends
from app.modules.auth.services.auth_service import get_current_user
from app.modules.dify.models.conversation_history import ConversationHistory
from app.core.config import settings
import httpx
from typing import  Optional

router = APIRouter()


@router.get("/")
async def get_conversation_history_messages(
    conversation_id: str,
    user: str,
    first_id: Optional[str] = None, # The ID of the first chat record on the current page, default is null
    limit: Optional[int] = 20, # How many chat history messages to return in one request, default is 20.
    username: str = Depends(get_current_user)
    ):
    try:
        # En-têtes pour l'API Dify
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        query = ""
        
        if not conversation_id:
             raise HTTPException(status_code=400, detail="Field conversation_id is required")
    
        if not user:
            raise HTTPException(status_code=400, detail="Field user is required")
        
        query += f"?user={user}&conversation_id={conversation_id}"
        
        if first_id:
            query += f"&first_id={first_id}"
        
        if limit:
            query += f"&limit={limit}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.DIFY_API_URL}/messages{query}", headers=headers)
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
        
