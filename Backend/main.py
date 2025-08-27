from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from dotenv import load_dotenv
import os

from app.core.db import connect_db
from app.api.v1.endpoints import auth, message
from app.core.socket import sio_app

load_dotenv()

PORT = int(os.getenv("PORT"))
ENV = os.getenv("NODE_ENV")

# Create FastAPI instance
app = FastAPI()

# Attach Socket.IO server to FastAPI
app.mount("/ws", sio_app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root API endpoint
@app.get("/", tags=["Root"])
async def chatapp():
    return {
        "name": "ChatApp API",
        "version": "1.0.0",
        "description": "Real-time chat application backend built with FastAPI",
        "features": [
            "Real-time messaging with Socket.IO",
            "JWT authentication",
            "User management",
            "Image sharing",
            "Online user tracking"
        ],
        "endpoints": {
            "auth": "/api/auth",
            "messages": "/api/messages",
            "websocket": "/ws"
        },
        "status": "running"
    }

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(message.router, prefix="/api/messages", tags=["Messages"])

# Serve static files in production
if ENV == "production":
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

    @app.get("/{full_path:path}")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))

# Startup event to connect DB
@app.on_event("startup")
async def startup():
    await connect_db()
