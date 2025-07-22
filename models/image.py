from sqlmodel import SQLModel, Field
from datetime import time, date
from uuid import UUID, uuid4

class Image(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    doctor_id: UUID
    image_path: str