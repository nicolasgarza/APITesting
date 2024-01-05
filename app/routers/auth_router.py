from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import SessionLocal
from app.crud import get_full_user_by_username, verify_password, hash_password
from app.schemas import Token
from jwt import verify_access_token, create_access_token

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

router = APIRouter()

@router.post("/login", response_model=None)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await get_full_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        secure=True,
        samesite='Lax'
    )
    return {"message": "Logged in successfully"}
