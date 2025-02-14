from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class ResponseMode(str, Enum):
    BLOCKING = "blocking"
    STREAMING = "streaming"

class TypeFile(str, Enum):
    DOCUMENT = "document"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    CUSTOM = "custom"

class TransfertMethod(str, Enum):
    REMOTE_URl = "remote_url"
    LOCAL_FILE = "local_file"
    
    
class File(BaseModel):
    type: Optional[TypeFile] = None
    transfer_method: Optional[TransfertMethod] = None
    url: Optional[str] = None
    upload_file_id: Optional[str] = None

class ChatMessage(BaseModel):
    inputs: dict
    query: str
    response_mode: ResponseMode
    conversation_id: str
    user: str
    files: Optional[List[File]] = None
    auto_generate_name: Optional[bool] = None



class DifyResponse(BaseModel):
    response: str