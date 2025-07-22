from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from Services.Auth import get_password_hash, verify_password
from interfaces.DoctorAuth import DoctorSignup
from interfaces.patient import PatientSignup
from models.DoctorAuth import DoctorAuth
from models.appointment import Appointment
from models.AppointmentForm import AppointmentForm
from models.doctor import Doctor
from models.image import Image
from sqlalchemy.future import select
from interfaces.AppointmentForm import CreateAppointmentForm
from interfaces.appointment import AppointmentCreate
from interfaces.doctor import CreateDoctor, UpdateDoctor
from sqlalchemy.exc import SQLAlchemyError

from models.patient import Patient
from models.chat import ChatMessage

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


async def get_doctor_by_id_async(db: AsyncSession, doctor_id: UUID):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    return result.scalar_one_or_none()


async def get_all_doctors_async(db: AsyncSession):
    result = await db.execute(select(Doctor))
    return result.scalars().all()


async def update_doctor_async(db: AsyncSession, doctor_id: UUID, request: UpdateDoctor):
    doctor = await get_doctor_by_id_async(db, doctor_id)
    if not doctor:
        return None

    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doctor, field, value)

    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor


async def delete_doctor_async(db: AsyncSession, doctor_id: UUID):
    doctor = await get_doctor_by_id_async(db, doctor_id)
    if not doctor:
        return None

    await db.delete(doctor)
    await db.commit()
    return True


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


async def signup_patient_async(db: AsyncSession, patient: PatientSignup):
    # Hash the patient's password before saving
    hashed_pw = get_password_hash(patient.password)

    # Create new PatientAuth entry
    db_patient = Patient(
        email=patient.email,
        name=patient.name,
        hashed_password=hashed_pw,
    )

    db.add(db_patient)
    try:
        await db.commit()
        await db.refresh(db_patient)
        return db_patient
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

# Asynchronous CRUD operation for Patient Login (authentication)


async def authenticate_patient_async(db: AsyncSession, email: str, password: str):
    # Get the patient from the database by their email
    patient = await db.execute(select(Patient).where(Patient.email == email))
    patient = patient.scalar_one_or_none()

    # If no patient found or password is incorrect
    if not patient or not verify_password(password, patient.hashed_password):
        return None

    return patient


async def get_all_patients_async(db: AsyncSession):
    from models.patient import Patient
    result = await db.execute(select(Patient))
    return result.scalars().all()


async def save_chat_message_async(db, sender_email: str, receiver_email: str, message: str):
    chat_message = ChatMessage(
        sender_email=sender_email, receiver_email=receiver_email, message=message)
    db.add(chat_message)
    await db.commit()
    await db.refresh(chat_message)
    return chat_message


async def get_chat_history_async(db, user1: str, user2: str):
    from sqlalchemy import or_, and_, select
    result = await db.execute(
        select(ChatMessage)
        .where(
            or_(
                and_(ChatMessage.sender_email == user1,
                     ChatMessage.receiver_email == user2),
                and_(ChatMessage.sender_email == user2,
                     ChatMessage.receiver_email == user1)
            )
        )
        .order_by(ChatMessage.timestamp)
    )
    return result.scalars().all()
