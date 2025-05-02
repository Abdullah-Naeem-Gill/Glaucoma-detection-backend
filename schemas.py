from pydantic import BaseModel, EmailStr
from datetime import time, date
from uuid import UUID


class BaseAppointment(BaseModel):
    name: str
    email: EmailStr
    phone: str
    time: time
    date: date


class AppointmentCreate(BaseAppointment):
    pass


class AppointmentRead(BaseAppointment):
    id: UUID


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


class ImageUploadResponse(BaseModel):
    doctor_id: UUID
    image_url: str
