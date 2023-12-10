from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from app.crud import get_comments, create_comment, update_comment, delete_comment
from app.models.base import SessionLocal
from app.schemas import Comment, CommentRead, CommentCreate, CommentUpdate

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/posts/{post_id}/comments", response_model=List[CommentRead])
async def get_comments_endpoint(post_id: int, session: AsyncSession = Depends(get_session)):
    comments = await get_comments(session, post_id)
    if comments is None:
        return []
    return [CommentRead(**comment.__dict__) for comment in comments]


@router.post("/posts/{post_id}/comments/{owner_id}", response_model=CommentRead)
async def post_comment_endpoint(post_id: int, owner_id: int, comment: CommentCreate, session: AsyncSession = Depends(get_session)):
    created_comment = await create_comment(post_id, owner_id, comment, session)
    if created_comment is None:
        return HTTPException(status_code=404, detail="Error creating comment")
    return Comment(**created_comment.__dict__)

@router.put("/comments/{comment_id}", response_model=CommentRead)
async def update_comment_endpoint(comment_id: int, comment: CommentUpdate, session: AsyncSession = Depends(get_session)):
    updated_comment = await update_comment(session, comment_id, comment)
    if update_comment is None:
        return HTTPException(status_code=404, detail="Comment not found")
    return Comment(**updated_comment.__dict__)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment_endpoint(comment_id: int, session: AsyncSession = Depends(get_session)):
    deleted_comment = await delete_comment(session, comment_id)
    if not deleted_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return {"detail": "Comment deleted successfully"}