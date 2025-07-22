import os
from fastapi import HTTPException
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:abdullah420@localhost:5432/glaucoma-detection")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    try:
        async with SessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=500, detail="Database connection error")


async def init_db() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            # Add email column to doctor table if it doesn't exist
            await add_email_column_to_doctor()
            # Add image_data column to chatmessage table if it doesn't exist
            await add_image_data_column_to_chatmessage()
    except SQLAlchemyError as e:
        logger.error(f"Error initializing the database: {e}")
        raise HTTPException(
            status_code=500, detail="Error initializing the database")
    else:
        logger.info("Database initialized successfully.")


async def add_email_column_to_doctor():
    """Add email column to doctor table if it doesn't exist"""
    try:
        async with engine.begin() as conn:
            # Check if email column exists
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'doctor' AND column_name = 'email'
            """))

            if not result.fetchone():
                # Add email column
                await conn.execute(text("ALTER TABLE doctor ADD COLUMN email VARCHAR(255)"))
                logger.info("Added email column to doctor table")
            else:
                logger.info("Email column already exists in doctor table")

    except SQLAlchemyError as e:
        logger.error(f"Error adding email column to doctor table: {e}")
        # Don't raise exception here as it might be a duplicate column error


async def add_image_data_column_to_chatmessage():
    """Add image_data column to chatmessage table if it doesn't exist"""
    try:
        async with engine.begin() as conn:
            # Check if image_data column exists
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'chatmessage' AND column_name = 'image_data'
            """))

            if not result.fetchone():
                # Add image_data column
                await conn.execute(text("ALTER TABLE chatmessage ADD COLUMN image_data TEXT"))
                logger.info("Added image_data column to chatmessage table")
            else:
                logger.info(
                    "Image_data column already exists in chatmessage table")

    except SQLAlchemyError as e:
        logger.error(
            f"Error adding image_data column to chatmessage table: {e}")
        # Don't raise exception here as it might be a duplicate column error
