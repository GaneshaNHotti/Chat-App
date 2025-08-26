# app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers import auth_controller
from app.middleware.auth_middleware import protect_route
from app.db import get_db

router = APIRouter()

@router.post("/signup")
async def signup_endpoint(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    return await auth_controller.signup(request, response, db)

@router.post("/login")
async def login_endpoint(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    return await auth_controller.login(request, response, db)

@router.post("/logout")
async def logout_endpoint(response: Response):
    return await auth_controller.logout(response)

@router.put("/update-profile")
async def update_profile_endpoint(request: Request, db: AsyncSession = Depends(get_db)):
    return await protect_route(auth_controller.update_profile)(request=request, db=db)

@router.get("/check")
async def check_auth_endpoint(request: Request):
    return await protect_route(auth_controller.check_auth)(request=request)
