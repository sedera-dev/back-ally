from fastapi import APIRouter, HTTPException, Depends
from app.modules.dify.models.chat_message import  ChatMessage
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import json
import httpx

router = APIRouter()


@router.post("/")
async def send_chat_message(
    chat_message: ChatMessage,
    username: str = Depends(get_current_user)
    ):
    try:
        # Headers for the Dify API
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # Payload pour l'API Dify
        payload = {
            "inputs": chat_message.inputs,
            "query": chat_message.query,
            "response_mode": chat_message.response_mode,
            "conversation_id": chat_message.conversation_id,
            "user": chat_message.user
        }
        
        if chat_message.auto_generate_name:
            payload["auto_generate_name"] = chat_message.auto_generate_name
        
        if chat_message.files:
            payload["files"] = [file.model_dump() for file in chat_message.files]
        
        
        if payload["response_mode"] == "blocking":
            # httpx.Client() is synchronous, so it waits for the Dify API to return a complete response before continuing
            timeout = httpx.Timeout(60.0, connect=30.0)
            with httpx.Client(timeout=timeout) as client:
                response = client.post(f"{settings.DIFY_API_URL}/chat-messages", json=payload, headers=headers)
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=response.text)
                return response.json()  

        elif payload["response_mode"] == "streaming":
            # httpx.AsyncClient() is asynchronous, which may not be compatible with blocking mode, because it does not stop waiting for a response
            async with  httpx.AsyncClient() as client:
                response = await client.post(f"{settings.DIFY_API_URL}/chat-messages", json=payload, headers=headers)
                
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=response.text)
                
                responses = []
                async for chunk in response.aiter_text():  # Read every piece of text in streaming
                    try:
                        # Trying to convert each piece of text to JSON
                        json_chunk = json.loads(chunk)
                        responses.append(json_chunk)
                    except json.JSONDecodeError:
                        # If the conversion fails, add the raw text
                        responses.append({"message": "Texte brut", "content": chunk})
                        
            return {"responses": responses}
        
        
        
       
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail= f"Error: {str(e)}"
        )
        
