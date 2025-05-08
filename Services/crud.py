from uuid import UUID
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.appointment import Appointment
from models.AppointmentForm import AppointmentForm
from models.doctor import Doctor
from models.image import Image
from sqlalchemy.future import select
from interfaces.AppointmentForm import CreateAppointmentForm
from interfaces.appointment import AppointmentCreate
from interfaces.doctor import CreateDoctor

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


async def save_image_record(db: Session, doctor_id: UUID, path: str):
    image = Image(doctor_id=doctor_id, image_path=path)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image_by_doctor_id(db: Session, doctor_id: UUID):
    result = await db.execute(select(Image).where(Image.doctor_id == doctor_id))
    return result.scalar_one_or_none()


async def create_appointment_form(db: AsyncSession, appointment: CreateAppointmentForm):
    db_appointment = AppointmentForm(
        firstName=appointment.firstName,
        lastName=appointment.lastName,
        dob=appointment.dob,
        phone=appointment.phone,
        email=appointment.email,
        reason=appointment.reason,
        preferredTime=appointment.preferredTime,
        preferredDate1=appointment.preferredDate1,
        preferredDate2=appointment.preferredDate2,
    )
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

async def get_appointments_form(db: AsyncSession):
    result = await db.execute(select(AppointmentForm))
    return result.scalars().all()
