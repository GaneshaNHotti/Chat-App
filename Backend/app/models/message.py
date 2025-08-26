from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
import uuid
from .base import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())