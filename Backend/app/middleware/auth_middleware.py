# app/middleware/auth_middleware.py
import os
import jwt
from fastapi import Request, HTTPException, Depends
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.models.user import User
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

# Add validation for JWT_SECRET
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is not set")

def protect_route(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        token = request.cookies.get("jwt")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized - No Token Provided")

        try:
            decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            
            # Get database session from kwargs or create new one
            db = None
            for key, value in kwargs.items():
                if isinstance(value, AsyncSession):
                    db = value
                    break
            
            if not db:
                # Create a new session if not found in kwargs
                from app.core.db import SessionLocal
                async with SessionLocal() as session:
                    result = await session.execute(
                        select(User).where(User.id == decoded["userId"])
                    )
                    user = result.scalar_one_or_none()
                    
                    if not user:
                        raise HTTPException(status_code=404, detail="User not found")

                    request.state.user = {
                        "id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                        "profile_pic": user.profile_pic
                    }
            else:
                result = await db.execute(
                    select(User).where(User.id == decoded["userId"])
                )
                user = result.scalar_one_or_none()
                
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")

                request.state.user = {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "profile_pic": user.profile_pic
                }

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Unauthorized - Token Expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Unauthorized - Invalid Token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        return await handler(*args, **kwargs)
    return wrapper
