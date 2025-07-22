from pydantic import BaseModel, EmailStr
from datetime import time, date
from uuid import UUID

class BaseAppointmentForm(BaseModel):
    firstName: str
    lastName: str
    dob: date
    phone: str
    email: str
    reason: str
    preferredTime: str
    preferredDate1: date
    preferredDate2: date


class CreateAppointmentForm(BaseAppointmentForm):
    pass


class ReadAppointmentForm(BaseAppointmentForm):
    id: UUID