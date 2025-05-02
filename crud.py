from sqlmodel import Session
from models import Appointment, Doctor
from sqlalchemy.future import select
from schemas import AppointmentCreate, CreateDoctor

async def create_appointment(db: Session, request: AppointmentCreate):
    appointment = Appointment(**request.dict())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def create_doctor(db: Session, request: CreateDoctor):
    new_doctor = Doctor(**request.dict())
    db.add(new_doctor)
    await db.commit()
    await db.refresh(new_doctor)
    return new_doctor


async def get_all_doctors(db: Session):
    result = await db.execute(select(Doctor))
    return result.scalars().all()