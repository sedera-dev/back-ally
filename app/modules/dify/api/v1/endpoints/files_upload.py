from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import httpx

router = APIRouter()

@router.post("/")
async def file_upload(
    file: UploadFile, 
    user: str = Form(...),  # Passer `user` comme un paramètre de formulaire
    type: str = Form(...),  # Passer `type` comme un paramètre de formulaire
    username: str = Depends(get_current_user)
):
    try:
        # En-têtes pour l'API Dify
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
        }
        
        # Payload pour l'API Dify
        files = {
            "file": (file.filename, file.file, file.content_type),
            "type": (None, type),
            "user": (None, user),
        }

        async with httpx.AsyncClient() as client:
            try:
                # Envoi du fichier avec httpx dans le corps multipart/form-data
                response = await client.post(f"{settings.DIFY_API_URL}/files/upload", files=files, headers=headers)
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
            detail=f"Error: {str(e)}"
        )
