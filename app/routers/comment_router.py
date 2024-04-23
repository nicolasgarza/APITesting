from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, AsyncGenerator
from app.crud import get_comment, get_comments, create_comment, update_comment, delete_comment
from app.models.base import SessionLocal
from app.schemas import Comment, CommentRead, CommentCreate, CommentUpdate, Token, CommentBase
from jwt import verify_access_token

router = APIRouter()

# Dependency to get the database session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/posts/{post_id}/comments", response_model=List[CommentRead])
async def get_comments_endpoint(post_id: int, session: AsyncSession = Depends(get_session)):
    comments = await get_comments(session, post_id)
    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comments found")
    return comments


@router.post("/posts/{post_id}/comments/{owner_id}", response_model=CommentRead)
async def post_comment_endpoint(post_id: int,
                                owner_id: int, 
                                comment: CommentBase, 
                                session: AsyncSession = Depends(get_session),
                                user: Token = Depends(verify_access_token)):
    if owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to post comment under different owner")
    created_comment = await create_comment(post_id, owner_id, comment, session)
    if created_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error creating comment")
    return created_comment

@router.put("/comments/{comment_id}", response_model=CommentRead)
async def update_comment_endpoint(comment_id: int,
                                  new_comment: CommentUpdate,
                                  session: AsyncSession = Depends(get_session),
                                  user: Token = Depends(verify_access_token)):
    comment = get_comment(session, comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if comment.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")
    updated_comment = await update_comment(session, comment_id, new_comment)
    return updated_comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment_endpoint(comment_id: int, 
                                  session: AsyncSession = Depends(get_session),
                                  user: Token = Depends(verify_access_token)):
    comment = get_comment(session, comment_id)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if comment.owner_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
    
    await delete_comment(session, comment_id)
    
    return {"detail": "Comment deleted successfully"}