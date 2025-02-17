from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form
from app.modules.auth.services.auth_service import get_current_user
from app.core.config import settings
import httpx

router = APIRouter()

@router.post("/")
async def file_upload(
    file: UploadFile, 
    user: str = Form(...),  # Passing `user` as a form parameter
    type: str = Form(...),  # Passing `type` as a form parameter
    username: str = Depends(get_current_user)
):
    try:
        # Headers for the Dify API
        headers = {
            "Authorization": f"Bearer {settings.DIFY_API_KEY}",
        }
        
        # Payload for Dify API
        files = {
            "file": (file.filename, file.file, file.content_type),
            "type": (None, type),
            "user": (None, user),
        }

        async with httpx.AsyncClient() as client:
            try:
                # Sending the file with httpx in the multipart/form-data body
                response = await client.post(f"{settings.DIFY_API_URL}/files/upload", files=files, headers=headers)
                response.raise_for_status()  # Throw an exception if the status is not 2xx
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Erreur lors de la communication avec l'API Dify: {e.response.text}",
                )

        # Return response from Dify API
        return response.json()
       
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error: {str(e)}"
        )
