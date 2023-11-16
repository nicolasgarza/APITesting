from fastapi import APIRouter
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 

from app.models.base import SessionLocal
from app.models import user_model  

router = APIRouter()

@router.get("/users")
async def read_users():
    return {"message": "List of all users"}

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id, "username": "Example User"}

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/test_db")
async def test_db(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))  
    return result.scalars().all()

@router.get("/items")
async def read_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(user_model.User)) 
    items = result.scalars().all()
    return items