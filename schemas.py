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