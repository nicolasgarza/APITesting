from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_post, get_posts, create_post, update_post, delete_post
from app.models.base import SessionLocal
from app.schemas import Post, PostRead, PostCreate, PostUpdate

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/posts/{post_id}", response_model=PostRead)
async def read_pos_endpoint(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await get_post(session, post_id)
    return result

@router.post("/posts", response_model=PostRead)
async def create_post_endpoint(post: PostCreate, session: AsyncSession = Depends(get_session)):
    created_post = await create_post(session, post)
    if created_post is None:
        raise HTTPException(status_code=400, detail="Error creating post")
    return created_post

@router.put("/posts/{post_id}", response_model=PostRead)
async def update_post_endpoint(post_id: int, post: PostUpdate, session: AsyncSession = Depends(get_session)):
    updated_post = await update_post(session, post_id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

@router.delete("/posts/{post_id}")
async def delete_user_endpoint(post_id: int, session: AsyncSession = Depends(get_session)):
    deleted_post = await delete_post(session, post_id)
    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return HTTPException(status_code=200, detail="Post deleted successfully")