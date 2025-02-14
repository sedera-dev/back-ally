from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from fastapi import UploadFile

class FilesUpload(BaseModel):
    user: str
    type: str