from sqlmodel import SQLModel, Field
from datetime import time, date
from uuid import UUID, uuid4

class AppointmentForm(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    firstName: str
    lastName: str
    dob: date
    phone: str
    email: str
    reason: str
    preferredTime: str
    preferredDate1: date
    preferredDate2: date