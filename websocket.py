# app/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()
active_connections = {}

async def connect_user(user_id: int, websocket: WebSocket):
    await websocket.accept()
    active_connections[user_id] = websocket

def disconnect_user(user_id: int):
    if user_id in active_connections:
        del active_connections[user_id]

async def notify_user(user_id: int, message: str):
    websocket = active_connections.get(user_id)
    if websocket:
        await websocket.send_text(message)

@ws_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await connect_user(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        disconnect_user(user_id)
