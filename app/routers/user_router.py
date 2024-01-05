from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from app.crud import get_user, create_user, update_user, delete_user
from app.models.base import SessionLocal
from app.schemas import User, UserCreate, UserUpdate, UserRead, Token
from jwt import verify_access_token

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/users/{user_id}", response_model=User)
async def get_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/users", response_model=UserRead)
async def create_user_endpoint(user: UserCreate, session: AsyncSession = Depends(get_session)):
    created_user = await create_user(session, user)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating user")
    return created_user

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user_endpoint(user: UserUpdate, user_id: int, session: AsyncSession = Depends(get_session),
                               verify_user: Token = Depends(verify_access_token)):
    updated_user = await update_user(session, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not Found")
    return User(**updated_user.__dict__)

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session),
                               user: Token = Depends(verify_access_token)):
    deleted_user = await delete_user(session, user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    return {"detail": "User deleted successfully"}
