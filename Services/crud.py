from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession  # Use AsyncSession for async DB operations
from Services.Auth import get_password_hash, verify_password
from interfaces.DoctorAuth import DoctorSignup
from models.DoctorAuth import DoctorAuth  # Correct - imports the class
from models.appointment import Appointment
from models.AppointmentForm import AppointmentForm
from models.doctor import Doctor
from models.image import Image
from sqlalchemy.future import select
from interfaces.AppointmentForm import CreateAppointmentForm
from interfaces.appointment import AppointmentCreate
from interfaces.doctor import CreateDoctor
from sqlalchemy.exc import SQLAlchemyError

# Asynchronous CRUD operations

async def create_appointment_async(db: AsyncSession, request: AppointmentCreate):
    appointment = Appointment(**request.dict())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def create_doctor_async(db: AsyncSession, request: CreateDoctor):
    new_doctor = Doctor(**request.dict())
    db.add(new_doctor)
    await db.commit()
    await db.refresh(new_doctor)
    return new_doctor


async def get_all_doctors_async(db: AsyncSession):
    result = await db.execute(select(Doctor))
    return result.scalars().all()


async def save_image_record_async(db: AsyncSession, doctor_id: UUID, path: str):
    image = Image(doctor_id=doctor_id, image_path=path)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image_by_doctor_id_async(db: AsyncSession, doctor_id: UUID):
    result = await db.execute(select(Image).where(Image.doctor_id == doctor_id))
    return result.scalar_one_or_none()


async def create_appointment_form_async(db: AsyncSession, appointment: CreateAppointmentForm):
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


async def get_appointments_form_async(db: AsyncSession):
    result = await db.execute(select(AppointmentForm))
    return result.scalars().all()


async def get_doctor_by_email_async(db: AsyncSession, email: str):
    result = await db.execute(select(DoctorAuth).where(DoctorAuth.email == email))
    return result.scalar_one_or_none()


async def signup_doctor_async(db: AsyncSession, doctor: DoctorSignup):
    hashed_pw = get_password_hash(doctor.password)
    db_doctor = DoctorAuth(
        email=doctor.email,
        name=doctor.name,
        specialization=doctor.specialization,
        hashed_password=hashed_pw,
    )
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    return db_doctor


async def authenticate_doctor_async(db: AsyncSession, email: str, password: str):
    doctor = await get_doctor_by_email_async(db, email)
    if not doctor:
        return None
    if not verify_password(password, doctor.hashed_password):
        return None
    return doctor
