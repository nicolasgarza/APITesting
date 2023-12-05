from typing import List, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_user(db: Session, user_id: int) -> Union[Dict[str, Any], None]:
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def create_user(db: Session, user: schemas.UserCreate) -> Dict[str, Any]:
    new_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Union[Dict[str, Any], None]:
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    old_user = result.scalars().first()
    if old_user:
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(old_user, key, value) if value is not None else None
        db.add(old_user)
        await db.commit()
        await db.refresh(old_user)
        return old_user
    return None


async def delete_user(db: Session, user_id: int) -> Union[Dict[str, Any], None]:
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    old_user = result.scalars().first()
    if old_user:
        await db.delete(old_user)
        await db.commit()
        return True
    return False

async def get_post(db: Session, id: int) -> Union[Dict[str, Any], None]:
    result = await db.execute(select(models.Post).filter(models.Post.id == id))
    return result.scalars().first()

def get_posts(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict[str, Any]], None]:
    return db.query(models.Post)\
            .filter(models.Post.owner_id == owner_id)\
            .order_by(models.Post.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

async def create_post(db: Session, post: schemas.PostCreate) -> Dict[str, Any]:
    new_post = models.Post(title=post.title, content=post.content, owner_id=post.owner_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

async def update_post(db: Session, id: int, post: schemas.PostUpdate) -> Union[Dict[str, Any], None]:
    result = await db.execute(select(models.Post).filter(models.Post.id == id))
    old_post = result.scalars().first()
    if old_post:
        update_data = post.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(old_post, key, value) if value is not None else None
        db.add(old_post)
        await db.commit()
        await db.refresh(old_post)
        return old_post
    return None

async def delete_post(db: Session, id: int) -> Union[Dict[str, Any], None]:
    result = await db.execute(select(models.Post).filter(models.Post.id == id))
    old_post = result.scalars().first()
    if old_post:
        await db.delete(old_post)
        await db.commit()
        return True
    return False

async def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict[str, Any]], None]:
    result = await db.execute(select(models.Comment).filter(models.Comment.post_id==post_id))
    comments = result.order_by(models.Comment.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    return comments

async def create_comment(post_id: int, owner_id: int, comment: schemas.CommentCreate, db: Session ) -> Dict[str, Any]:
    new_comment = models.Comment(content=comment.content, post_id=post_id, owner_id=owner_id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

def update_comment(db: Session, id: int, comment: schemas.CommentUpdate) -> Union[Dict[str, Any], None]:
    old_comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if old_comment:
        if comment.content:
            old_comment.content = comment.content
        db.add(old_comment)
        db.commit()
        db.refresh(old_comment)
        return old_comment
    return None

def delete_comment(db: Session, id: int) -> Union[Dict[str, Any], None]:
    old_comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if old_comment:
        db.delete(old_comment)
        db.commit()
        return True
    return False
