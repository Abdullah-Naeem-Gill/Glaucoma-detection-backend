from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Services.Auth import create_access_token, verify_role
from Services.crud import (
    authenticate_doctor_async,
    get_doctor_by_email_async,
    signup_doctor_async
)
from Core.database import get_db
from interfaces.DoctorAuth import DoctorLogin, DoctorOut, DoctorSignup, Token

router = APIRouter(prefix="/doctorauth", tags=["DoctorsAuth"])


@router.post("/signup", response_model=DoctorOut)
async def signup(doctor: DoctorSignup, db: AsyncSession = Depends(get_db)):
    existing = await get_doctor_by_email_async(db, doctor.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_doctor = await signup_doctor_async(db, doctor)
    print(f"[Email to {doctor.email}] Click here to verify your account.")

    return new_doctor


@router.post("/login", response_model=Token)
async def login(doctor: DoctorLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_doctor_async(db, doctor.email, doctor.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    token_data = {
        "sub": user.email,
        "role": "doctor"
    }
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "doctor_id": str(user.id),
        "email": user.email
    }
