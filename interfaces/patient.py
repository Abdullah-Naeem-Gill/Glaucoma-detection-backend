from uuid import UUID
from pydantic import BaseModel, EmailStr


class PatientSignup(BaseModel):
    email: EmailStr
    name: str
    password: str


class PatientLogin(BaseModel):
    email: EmailStr
    password: str


class PatientOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    is_verified: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    patient_id: str | None = None
    email: str | None = None
