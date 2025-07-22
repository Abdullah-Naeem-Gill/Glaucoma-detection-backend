from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from Core.database import init_db
from controllers import chat
from controllers import AppointmentForm, DoctorAuth, appointment, doctor, image, patient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(appointment.router)
app.include_router(doctor.router)
app.include_router(image.router)
app.include_router(AppointmentForm.router)
app.include_router(DoctorAuth.router)
app.include_router(patient.router)
app.include_router(chat.router)
