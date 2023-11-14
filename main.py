from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Import the select function

# Import your database session and models
from app.models.base import SessionLocal
from app.models import user_model  # Replace with your actual models

from app.routers import post_router, user_router, comment_router

app = FastAPI()

app.include_router(post_router.router)
app.include_router(user_router.router)
app.include_router(comment_router.router)