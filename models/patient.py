from uuid import UUID, uuid4
from pydantic import EmailStr, Field
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Patient(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )
    email: EmailStr = Field(..., unique=True)  # Ellipsis (...) makes it required
    name: str = Field(...)
    hashed_password: str = Field(...)
    is_verified: bool = Field(default=True)