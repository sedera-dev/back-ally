
import uvicorn
from fastapi import FastAPI
from app.modules.auth.api.v1.endpoints.router import router as auth_router
from app.modules.dify.api.v1.endpoints.router import router as dify_router
from app.core.config import settings
import os

version = "v1"

app = FastAPI(
    title="Ally",
    description="A REST API for Ally",
    version=version
)
    
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentification"])
app.include_router(dify_router, prefix=f"/api/{version}/dify", tags=["Dify API"])


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)