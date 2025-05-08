from pydantic import BaseModel, EmailStr
from datetime import time, date
from uuid import UUID

class BaseDoctor(BaseModel):
    name: str
    profession: str
    experience: int
    gender: str
    rating: int
    available_time: str
    fees: int


class CreateDoctor(BaseDoctor):
    pass


class ReadDoctor(BaseDoctor):
    id: UUID