from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Services.Auth import create_access_token, verify_role
from Services.crud import (
    authenticate_patient_async,
    signup_patient_async,
    get_all_patients_async,  # <-- import the new function
)
from Core.database import get_db
from interfaces.patient import PatientSignup, PatientLogin, Token, PatientOut
from typing import List

router = APIRouter(prefix="/patientauth", tags=["PatientsAuth"])


# Patient Signup Endpoint
@router.post("/signup", response_model=PatientOut)
async def signup(patient: PatientSignup, db: AsyncSession = Depends(get_db)):
    # Sign up the patient
    new_patient = await signup_patient_async(db, patient)
    # Email verification logic can be added
    print(f"[Email to {patient.email}] Click here to verify your account.")

    return new_patient


# Patient Login Endpoint
@router.post("/login", response_model=Token)
async def login(patient: PatientLogin, db: AsyncSession = Depends(get_db)):
    # Authenticate patient by email and password
    db_patient = await authenticate_patient_async(db, patient.email, patient.password)
    if not db_patient:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Prepare data for generating token
    token_data = {
        "sub": db_patient.email,
        "role": "patient"
    }
    # Create access token
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "patient_id": str(db_patient.id),
        "email": db_patient.email
    }

# Endpoint to fetch all patients


@router.get("/", response_model=List[PatientOut])
async def list_patients(db: AsyncSession = Depends(get_db)):
    return await get_all_patients_async(db)
