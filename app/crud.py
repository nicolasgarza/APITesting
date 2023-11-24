
from typing import List, Dict, Any, Union
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int) -> Union[Dict[str, Any], None]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate) -> Dict[str, Any]:
    new_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Union[Dict[str, Any], None]:
    old_user = db.query(models.User).filter(models.User.id == user_id).first()
    if old_user:
        if user.username:
            old_user.username = user.username
        if user.email:
            old_user.email = user.email
        if user.password:
            old_user.hashed_password = user.password
        db.add(old_user)
        db.commit()
        db.refresh(old_user)
        return old_user
    return None


def delete_user(db: Session, user_id: int) -> Union[Dict[str, Any], None]:
    old_user = db.query(models.User).filter(models.User.id == user_id).first()
    if old_user:
        db.delete(old_user)
        db.commit()
        return True
    return False

def get_post(db: Session, id: int) -> Union[Dict[str, Any], None]:
    return db.query(models.Post).filter(models.Post.id == id).first()

def get_posts(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict[str, Any]], None]:
    return db.query(models.Post)\
            .filter(models.Post.owner_id == owner_id)\
            .order_by(models.Post.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

def create_post(db: Session, owner_id: int, post: schemas.PostCreate) -> Dict[str, Any]:
    new_post = models.Post(title=post.title, content=post.content, owner_id=owner_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def update_post(db: Session, id: int, post: schemas.PostUpdate) -> Union[Dict[str, Any], None]:
    old_post = db.query(models.Post).filter(models.Post.id == id).first()
    if old_post:
        if post.title:
            old_post.title = post.title
        if post.content:
            old_post.content = post.content
        db.add(old_post)
        db.commit()
        db.refresh(old_post)
        return old_post
    return None

def delete_post(db: Session, id: int) -> Union[Dict[str, Any], None]:
    old_post = db.query(models.Post).filter(models.Post.id == id).first()
    if old_post:
        db.delete(old_post)
        db.commit()
        return True
    return False

def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict[str, Any]], None]:
    return db.query(models.Comment)\
            .filter(models.Comment.post_id == post_id)\
            .order_by(models.Comment.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

def create_comment(db: Session, post_id: int, owner_id: int, comment: schemas.CommentCreate) -> Dict[str, Any]:
    new_comment = models.Comment(content=comment.content, post_id=post_id, owner_id=owner_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
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
