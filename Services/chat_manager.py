from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # key: user email

    async def connect(self, user_email: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_email] = websocket

    def disconnect(self, user_email: str):
        self.active_connections.pop(user_email, None)

    async def send_personal_message(self, message: str, user_email: str):
        websocket = self.active_connections.get(user_email)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str, user_emails: List[str]):
        for email in user_emails:
            await self.send_personal_message(message, email)
