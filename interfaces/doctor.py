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

class UpdateDoctor(BaseModel):
    name: str | None = None
    profession: str | None = None
    experience: int | None = None
    gender: str | None = None
    rating: int | None = None
    available_time: str | None = None
    fees: int | None = None