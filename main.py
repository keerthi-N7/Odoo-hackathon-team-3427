from fastapi import FastAPI
from app import models
from app.database import engine
from app.auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/api/auth")
from fastapi.middleware.cors import CORSMiddleware
from app.profile import router as profile_router
from app.auth import router as auth_router
from app.swap import router as swap_router


app = FastAPI()

# CORS (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(profile_router, prefix="/api/profile")
app.include_router(swap_router)
from app.websocket import ws_router
app.include_router(ws_router)
from fastapi import WebSocket, WebSocketDisconnect
from app.websocket import ws_router

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await connect_user(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep the connection alive
    except WebSocketDisconnect:
        disconnect_user(user_id)
from fastapi import FastAPI
from app.websocket import ws_router
app.include_router(ws_router)


