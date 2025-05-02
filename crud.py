from sqlmodel import Session
from models import Appointment
from schemas import AppointmentCreate

async def create_appointment(db: Session, data: AppointmentCreate):
    appointment = Appointment(**data.dict())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment
