from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class ChatMessage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    sender_email: str
    receiver_email: str
    message: str
    image_data: Optional[str] = None  # Base64 encoded image data
    timestamp: datetime = Field(default_factory=datetime.utcnow)
