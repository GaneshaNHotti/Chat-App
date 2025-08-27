import os
import jwt
from fastapi import Response
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
    response.set_cookie(
        key="jwt",
        value=token,
        max_age=JWT_EXPIRY,
        httponly=True,  # prevent XSS attacks
        samesite="strict",  # protect against CSRF
        secure=(os.getenv("NODE_ENV") != "development")  # only HTTPS if not dev
    )