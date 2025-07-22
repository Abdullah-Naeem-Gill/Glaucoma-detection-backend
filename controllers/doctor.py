from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from Core.database import get_db
from Services.Auth import verify_role
from interfaces.doctor import CreateDoctor, ReadDoctor, UpdateDoctor
from Services.crud import (
    create_doctor_async, 
    get_all_doctors_async, 
    get_doctor_by_id_async,
    update_doctor_async,
    delete_doctor_async
)

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

@router.get("/{doctor_id}", response_model=ReadDoctor)
async def get_doctor(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(verify_role(is_doctor=True))
):
    doctor = await get_doctor_by_id_async(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=ReadDoctor)
async def update_doctor(
    doctor_id: str,
    doctor_data: UpdateDoctor,
    db: AsyncSession = Depends(get_db),
    user=Depends(verify_role(is_doctor=True))
):
    updated_doctor = await update_doctor_async(db, doctor_id, doctor_data)
    if not updated_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated_doctor

@router.delete("/{doctor_id}")
async def delete_doctor(
    doctor_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(verify_role(is_doctor=True))
):
    success = await delete_doctor_async(db, doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}