from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from app.models.base import SessionLocal
from app.models.user_model import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = ''
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

db_session = Annotated[AsyncSession, Depends(get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(request: CreateUserRequest, session: AsyncSession = db_session):
    user = User(username=request.username, email=request.email, hashed_password=bcrypt_context.hash(request.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user