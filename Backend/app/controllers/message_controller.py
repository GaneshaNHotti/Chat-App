# app/controllers/message_controller.py
from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db import get_db
from app.models.user import User
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse
from app.schemas.user import UserResponse
import cloudinary.uploader
from app.core.socket import get_receiver_socket_id, sio
from typing import List

async def get_users_for_sidebar(request: Request, db: AsyncSession = Depends(get_db)) -> List[UserResponse]:
    logged_in_user_id = request.state.user["id"]
    
    result = await db.execute(
        select(User).where(User.id != logged_in_user_id)
    )
    users = result.scalars().all()
    
    return [
        UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            profile_pic=user.profile_pic,
            created_at=user.created_at
        ) for user in users
    ]

async def get_messages(request: Request, id: str, db: AsyncSession = Depends(get_db)) -> List[MessageResponse]:
    my_id = request.state.user["id"]
    
    result = await db.execute(
        select(Message).where(
            or_(
                (Message.sender_id == my_id) & (Message.receiver_id == id),
                (Message.sender_id == id) & (Message.receiver_id == my_id)
            )
        ).order_by(Message.created_at)
    )
    messages = result.scalars().all()
    
    return [
        MessageResponse(
            id=message.id,
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            text=message.text,
            image=message.image,
            created_at=message.created_at
        ) for message in messages
    ]

async def send_message(request: Request, id: str, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    data = await request.json()
    message_data = MessageCreate(**data)
    sender_id = request.state.user["id"]

    image_url = None
    if message_data.image:
        upload_response = cloudinary.uploader.upload(message_data.image)
        image_url = upload_response["secure_url"]

    new_message = Message(
        sender_id=sender_id,
        receiver_id=id,
        text=message_data.text,
        image=image_url
    )
    
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    message_response = MessageResponse(
        id=new_message.id,
        sender_id=new_message.sender_id,
        receiver_id=new_message.receiver_id,
        text=new_message.text,
        image=new_message.image,
        created_at=new_message.created_at
    )

    # Send to receiver via socket
    receiver_socket_id = get_receiver_socket_id(id)
    if receiver_socket_id:
        await sio.emit("newMessage", message_response.dict(), to=receiver_socket_id)

    return message_response
