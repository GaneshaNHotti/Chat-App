# app/controllers/auth_controller.py
import os
import bcrypt
import jwt
from fastapi import Request, Response, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserResponse
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRY = 60 * 60 * 24 * 7  # 7 days

# Add validation for JWT_SECRET
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is not set")

def generate_token(user_id: str, response: Response):
    token = jwt.encode({"userId": user_id}, JWT_SECRET, algorithm="HS256")
    response.set_cookie(key="jwt", value=token, httponly=True, max_age=JWT_EXPIRY)

async def signup(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    user_data = UserCreate(**data)

    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password
    hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt())

    # Create user
    new_user = User(
        full_name=user_data.fullName,
        email=user_data.email,
        password=hashed_password.decode("utf-8")
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    generate_token(new_user.id, response)

    return UserResponse(
        id=new_user.id,
        full_name=new_user.full_name,
        email=new_user.email,
        profile_pic=new_user.profile_pic,
        created_at=new_user.created_at
    )

async def login(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    login_data = UserLogin(**data)

    # Find user
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()
    
    if not user or not bcrypt.checkpw(login_data.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    generate_token(user.id, response)

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        profile_pic=user.profile_pic,
        created_at=user.created_at
    )

async def logout(response: Response):
    response.delete_cookie("jwt")
    return {"message": "Logged out successfully"}

async def update_profile(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    update_data = UserUpdate(**data)
    user = request.state.user

    if not update_data.profilePic:
        raise HTTPException(status_code=400, detail="Profile pic is required")

    # Upload to cloudinary
    upload_response = cloudinary.uploader.upload(update_data.profilePic)
    
    # Update user
    result = await db.execute(select(User).where(User.id == user["id"]))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.profile_pic = upload_response["secure_url"]
    await db.commit()
    await db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        full_name=db_user.full_name,
        email=db_user.email,
        profile_pic=db_user.profile_pic,
        created_at=db_user.created_at
    )

async def check_auth(request: Request):
    return request.state.user
