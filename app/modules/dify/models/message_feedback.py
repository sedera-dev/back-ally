from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Rating(str,Enum):
    LIKE = "like",
    DISLIKE = "dislike"

class MessageFeedBack(BaseModel):
    rating: Rating
    user: str
    content: str