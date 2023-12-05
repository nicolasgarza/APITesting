from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_comments, create_comment, update_comment, delete_comment
from app.models.base import SessionLocal
from app.schemas import Comment, CommentRead, CommentCreate

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.post("/posts/{post_id}/comments/{owner_id}", response_model=CommentRead)
async def post_comment_endpoint(post_id: int, owner_id: int, comment: CommentCreate,  session: AsyncSession = Depends(get_session),):
    created_comment = await create_comment(post_id, owner_id, comment, session)
    if created_comment is None:
        return HTTPException(status_code=404, detail="Error creating comment")
    return created_comment
