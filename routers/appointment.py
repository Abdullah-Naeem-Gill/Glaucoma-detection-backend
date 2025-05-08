from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Core.database import get_db
from interfaces.appointment import AppointmentCreate, AppointmentRead
from Services.crud import create_appointment

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model= AppointmentRead)
async def book_appointment(
    request: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_appointment(db, request)
