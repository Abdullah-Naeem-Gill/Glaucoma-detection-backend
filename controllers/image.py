from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from uuid import UUID
from fastapi.responses import FileResponse
import aiofiles

from Core.database import get_db
from Services.Auth import verify_role
from Services.crud import save_image_record_async, get_image_by_doctor_id_async
from models.doctor import Doctor
from interfaces.image import ImageUploadResponse
from sqlalchemy import select

router = APIRouter(prefix="/images", tags=["Images"])

IMAGE_UPLOAD_DIR = Path("static/images")
IMAGE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/{doctor_id}", response_model=ImageUploadResponse)
async def upload_image(
    doctor_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(verify_role(is_doctor=True))
):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    file_path = IMAGE_UPLOAD_DIR / f"{doctor_id}.jpg"
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    image = await save_image_record_async(db, doctor_id, str(file_path))
    return ImageUploadResponse(doctor_id=doctor_id, image_url=f"/images/get/{doctor_id}")


@router.get("/get/{doctor_id}")
async def get_image(
    doctor_id: UUID,
    db: AsyncSession = Depends(get_db)

):
    image = await get_image_by_doctor_id_async(db, doctor_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    image_path = Path(image.image_path)
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image file missing")

    return FileResponse(image_path)
