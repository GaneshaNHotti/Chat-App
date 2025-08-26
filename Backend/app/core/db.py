import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost:5432/chatapp")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def connect_db():
    try:
        await create_tables()
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)  # simple ping
        print("✅ Database connected and tables created")
    except Exception as e:
        print("❌ Database connection failed:", e)
