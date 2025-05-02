from sqlmodel import SQLModel, Field
from datetime import time, date
from uuid import UUID,uuid4

class Appointment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    email: str
    phone: str
    time: time
    date: date
