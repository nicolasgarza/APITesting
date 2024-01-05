from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from app.crud import get_post, get_posts, create_post, update_post, delete_post
from app.models.base import SessionLocal
from app.schemas import Post, PostRead, PostCreate, PostUpdate, Token
from jwt import verify_access_token

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/posts/{post_id}", response_model=PostRead)
async def read_post_endpoint(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await get_post(session, post_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")    
    return result

@router.get("/users/{user_id}/posts", response_model=List[PostRead])
async def read_users_posts_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await get_posts(session, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found")
    return result

@router.post("/posts", response_model=PostRead)
async def create_post_endpoint(post: PostCreate, 
                               session: AsyncSession = Depends(get_session),
                               user: Token = Depends(verify_access_token)
                               ):
    if post.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create post under another user")
    created_post = await create_post(session, post)
    if created_post is None:
        raise HTTPException(status_code=400, detail="Error creating post")
    return created_post

@router.put("/posts/{post_id}", response_model=PostRead)
async def update_post_endpoint(post_id: int, new_post: PostUpdate, 
                               session: AsyncSession = Depends(get_session),
                               user: Token = Depends(verify_access_token)
                               ):
    post = await get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    updated_post = await update_post(session, post_id, new_post)
    
    return updated_post

@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post_endpoint(post_id: int, 
                               session: AsyncSession = Depends(get_session),
                               user: Token = Depends(verify_access_token)):
    post = await get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    
    await delete_post(session, post_id)

    return {"detail": "Post deleted successfully"}