from fastapi import APIRouter, HTTPException, Depends
from app.modules.dify.models.chat_message import  ChatMessage
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import json
import httpx

router = APIRouter()


@router.post("/chat-messages")
async def chat_messages(
    user_message: ChatMessage,
    username: str = Depends(get_current_user)
    ):
    try:
        # En-têtes pour l'API Dify
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # Payload pour l'API Dify
        payload = {
            "inputs": user_message.inputs,
            "query": user_message.query,
            "response_mode": user_message.response_mode,
            "conversation_id": user_message.conversation_id,
            "user": user_message.user
        }
        
        if user_message.auto_generate_name:
            payload["auto_generate_name"] = user_message.auto_generate_name
        
        if user_message.files:
            payload["files"] = [file.model_dump() for file in user_message.files]
        
        print(f" PAYLOAD: {payload}")
        
        if payload["response_mode"] == "blocking":
            # httpx.Client() est synchrone, donc il attend que l'API Dify renvoie une réponse complète avant de continuer
            timeout = httpx.Timeout(60.0, connect=30.0)
            with httpx.Client(timeout=timeout) as client:
                response = client.post(f"{settings.DIFY_API_URL}/chat-messages", json=payload, headers=headers)
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=response.text)
                return response.json()  

        elif payload["response_mode"] == "streaming":
            # httpx.AsyncClient() est asynchrone, ce qui peut ne pas être compatible avec le mode blocking, car il ne s'arrête pas d'attendre une réponse
            async with  httpx.AsyncClient() as client:
                response = await client.post(f"{settings.DIFY_API_URL}/chat-messages", json=payload, headers=headers)
                
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=response.text)
                
                responses = []
                async for chunk in response.aiter_text():  # Lire chaque morceau de texte en streaming
                    try:
                        # Essayer de convertir chaque morceau de texte en JSON
                        json_chunk = json.loads(chunk)
                        responses.append(json_chunk)
                    except json.JSONDecodeError:
                        # Si la conversion échoue, on ajoute le texte brut
                        responses.append({"message": "Texte brut", "content": chunk})
                        
            return {"responses": responses}
        
        
        
       
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail= f"Error: {str(e)}"
        )
        
