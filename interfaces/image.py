from pydantic import BaseModel, EmailStr
from datetime import time, date
from uuid import UUID


class ImageUploadResponse(BaseModel):
    doctor_id: UUID
    image_url: str