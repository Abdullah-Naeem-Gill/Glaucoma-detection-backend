from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Services.Auth import create_access_token, verify_role
from Services.crud import (
    authenticate_patient_async,
    signup_patient_async,
)
from Core.database import get_db
from interfaces.patient import PatientSignup, PatientLogin, Token, PatientOut

router = APIRouter(prefix="/patientauth", tags=["PatientsAuth"])


# Patient Signup Endpoint
@router.post("/signup", response_model=PatientOut)
async def signup(patient: PatientSignup, db: AsyncSession = Depends(get_db)):
    # Sign up the patient
    new_patient = await signup_patient_async(db, patient)
    print(f"[Email to {patient.email}] Click here to verify your account.")  # Email verification logic can be added

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

    return {"access_token": access_token, "token_type": "bearer"}
