from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    text: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True