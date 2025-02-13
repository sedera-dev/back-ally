
from pydantic import BaseModel

class UserMessage(BaseModel):
    inputs: dict
    query: str
    response_mode: str
    conversation_id: str
    user: str

class DifyResponse(BaseModel):
    response: str