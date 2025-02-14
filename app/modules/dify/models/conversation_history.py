from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ConversationHistory(BaseModel):
    conversation_id: str
    user: str
    first_id: Optional[str] = None # The ID of the first chat record on the current page, default is null
    limit: Optional[int] = 20 # How many chat history messages to return in one request, default is 20.