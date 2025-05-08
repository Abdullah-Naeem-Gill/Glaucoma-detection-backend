from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ import CORS middleware

from Core.database import init_db
from routers import AppointmentForm, appointment, doctor, image

app = FastAPI()

# ✅ Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000"],  # <-- update this line
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(appointment.router)
app.include_router(doctor.router)
app.include_router(image.router)
app.include_router(AppointmentForm.router)