#!/usr/bin/env python3
"""
Database initialization script
Run this to create the database tables
"""

import asyncio
import os
from dotenv import load_dotenv
from app.core.db import connect_db

async def main():
    load_dotenv()
    print("Initializing database...")
    await connect_db()
    print("Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(main())