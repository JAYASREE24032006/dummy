from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.auth.websockets import sio_app

app = FastAPI(title="Agentic SSO")

# CORS Configuration
# Relaxing CORS to allow all local development origins via Regex
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO

# Remove this mount
# app.mount("/ws", sio_app)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Agentic SSO System Active"}

# Wrap FastAPI with Socket.IO
from app.auth.websockets import sio_server
import socketio
app = socketio.ASGIApp(sio_server, app)
# Backend Reload Triggered Again

