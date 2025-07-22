from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status, HTTPException
from Services.chat_manager import ConnectionManager
from Services.Auth import decode_access_token
from Services.image_utils import validate_image_data, clean_image_data
from jose import JWTError
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from Services.crud import save_chat_message_async, get_chat_history_async
from Core.database import get_db
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
import asyncio
from sqlmodel import SQLModel
from models.chat import ChatMessage
from Core.database import engine
import json

router = APIRouter(prefix="/ws", tags=["Chat"])
manager = ConnectionManager()

# Store user connections with additional info
user_connections: Dict[str, Dict] = {}


class ChatMessageOut(BaseModel):
    id: UUID
    sender_email: str
    receiver_email: str
    message: str
    image_data: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class ImageTestRequest(BaseModel):
    image_data: str


def get_email_from_token(token: str):
    try:
        payload = decode_access_token(token)
        if not payload:
            return None, None
        return payload.get("sub"), payload.get("role")
    except JWTError:
        return None, None


@router.get("/test")
async def test_chat():
    """Test endpoint to verify chat system is working"""
    return {"message": "Chat system is active", "active_connections": len(manager.active_connections)}


@router.post("/test-image")
async def test_image_validation(request: ImageTestRequest):
    """Test endpoint to validate image data"""
    from Services.image_utils import validate_image_data, get_image_format

    is_valid, error_msg = validate_image_data(request.image_data)
    if is_valid:
        format_type = get_image_format(request.image_data)
        return {
            "valid": True,
            "format": format_type,
            "message": "Image is valid"
        }
    else:
        return {
            "valid": False,
            "error": error_msg
        }


@router.get("/active-users")
async def get_active_users():
    """Get list of active users for chat"""
    active_users = []
    for email, info in user_connections.items():
        active_users.append({
            "email": email,
            "role": info["role"]
        })
    return {"active_users": active_users}


@router.get("/history/{user1_email}/{user2_email}", response_model=List[ChatMessageOut])
async def get_chat_history(user1_email: str, user2_email: str, db: AsyncSession = Depends(get_db)):
    return await get_chat_history_async(db, user1_email, user2_email)


@router.websocket("/chat")
async def chat_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    # Expect token as query param: ws://.../ws/chat?token=xxx
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_email, role = get_email_from_token(token)
    if not user_email or role not in ("doctor", "patient"):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user_email, websocket)
    user_connections[user_email] = {"role": role, "email": user_email}

    try:
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "info",
            "message": f"Connected as {role}: {user_email}",
            "sender_email": user_email
        }))

        while True:
            data = await websocket.receive_json()
            # data: { "to": "other_user_email", "message": "...", "image_data": "base64_string" (optional) }
            to_email = data.get("to")
            message = data.get("message")
            image_data = data.get("image_data")  # Optional base64 image data

            # Validate image data if provided
            if image_data:
                is_valid, error_msg = validate_image_data(image_data)
                if not is_valid:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": error_msg,
                        "sender_email": user_email
                    }))
                    continue
                # Clean the image data (remove data URL prefix if present)
                image_data = clean_image_data(image_data)

            if to_email and (message or image_data):
                # Send to receiver as 'received'
                await manager.send_personal_message(json.dumps({
                    "sender_email": user_email,
                    "receiver_email": to_email,
                    "message": message,
                    "image_data": image_data,
                    "type": "received"
                }), to_email)
                # Send to sender as 'sent'
                await websocket.send_text(json.dumps({
                    "sender_email": user_email,
                    "receiver_email": to_email,
                    "message": message,
                    "image_data": image_data,
                    "type": "sent"
                }))
                # Save message to DB
                await save_chat_message_async(db, user_email, to_email, message, image_data)
    except WebSocketDisconnect:
        manager.disconnect(user_email)
        user_connections.pop(user_email, None)
