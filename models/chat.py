from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class ChatMessage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    sender_email: str
    receiver_email: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
