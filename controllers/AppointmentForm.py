from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import interfaces.AppointmentForm as schemas
import Services.crud as crud
from Core.database import get_db

router = APIRouter(
    prefix="/appointment/form",
    tags=["appointments form"]
)

@router.post("/", response_model=schemas.ReadAppointmentForm)
async def appointment_form(
    appointment: schemas.CreateAppointmentForm,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_appointment_form_async(db, appointment)

@router.get("/", response_model=List[schemas.ReadAppointmentForm])
async def read_appointments_form(db: AsyncSession = Depends(get_db)):
    return await crud.get_appointments_form_async(db)
