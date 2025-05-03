from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud, models
from database import get_db

router = APIRouter(
    prefix="/appointment/form",
    tags=["appointments form"]
)

@router.post("/", response_model=schemas.ReadAppointmentForm)
async def appointment_form(appointment: schemas.CreateAppointmentForm, db: AsyncSession = Depends(get_db)):
    return await crud.create_appointment_form(db, appointment)

@router.get("/", response_model=List[schemas.ReadAppointmentForm])
async def read_appointments_form(db: AsyncSession = Depends(get_db)):
    return await crud.get_appointments_form(db)

