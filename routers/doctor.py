from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from Core.database import get_db
from interfaces.doctor import CreateDoctor, ReadDoctor
from Services.crud import create_doctor, get_all_doctors
from typing import List

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=ReadDoctor)
async def add_doctor(doctor: CreateDoctor, db: AsyncSession = Depends(get_db)):
    return await create_doctor(db, doctor)

@router.get("/", response_model=List[ReadDoctor])
async def list_doctors(db: AsyncSession = Depends(get_db)):
    return await get_all_doctors(db)
