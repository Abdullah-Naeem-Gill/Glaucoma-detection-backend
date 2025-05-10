from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from Core.database import get_db
from Services.Auth import verify_role
from interfaces.doctor import CreateDoctor, ReadDoctor
from Services.crud import create_doctor_async, get_all_doctors_async

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=ReadDoctor)
async def add_doctor(
    doctor: CreateDoctor,
    db: AsyncSession = Depends(get_db),
    user=Depends(verify_role(is_doctor=True))
):
    return await create_doctor_async(db, doctor)

@router.get("/", response_model=List[ReadDoctor])
async def list_doctors(db: AsyncSession = Depends(get_db)):
    return await get_all_doctors_async(db)
