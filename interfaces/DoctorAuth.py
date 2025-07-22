from uuid import UUID
from pydantic import BaseModel, EmailStr


class DoctorSignup(BaseModel):
    email: EmailStr
    name: str
    specialization: str
    password: str


class DoctorLogin(BaseModel):
    email: EmailStr
    password: str


class DoctorOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    specialization: str
    is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    doctor_id: str | None = None
    email: str | None = None
