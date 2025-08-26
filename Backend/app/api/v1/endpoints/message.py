# app/api/v1/endpoints/message.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers import message_controller
from app.middleware.auth_middleware import protect_route
from app.db import get_db

router = APIRouter()

@router.get("/users")
async def get_users_endpoint(request: Request, db: AsyncSession = Depends(get_db)):
    return await protect_route(message_controller.get_users_for_sidebar)(request=request, db=db)

@router.get("/{id}")
async def get_messages_endpoint(request: Request, id: str, db: AsyncSession = Depends(get_db)):
    return await protect_route(message_controller.get_messages)(request=request, id=id, db=db)

@router.post("/send/{id}")
async def send_message_endpoint(request: Request, id: str, db: AsyncSession = Depends(get_db)):
    return await protect_route(message_controller.send_message)(request=request, id=id, db=db)
