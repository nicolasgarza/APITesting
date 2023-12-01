from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_user, create_user, update_user, delete_user
from app.models.base import SessionLocal
from app.schemas import User, UserCreate, UserUpdate, UserRead

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/users/{user_id}", response_model=User)
async def get_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserRead)
async def create_user_endpoint(user: UserCreate, session: AsyncSession = Depends(get_session)):
    created_user = await create_user(session, user)
    if create_user is None:
        raise HTTPException(status_code=400, detail="Error creating user")
    return created_user

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user_endpoint(user: UserUpdate, user_id: int, session: AsyncSession = Depends(get_session)):
    updated_user = await update_user(session, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not Found")
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    deleted_user = await delete_user(session, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not Found")
    return HTTPException(status_code=204, detail="User deleted successfully")
