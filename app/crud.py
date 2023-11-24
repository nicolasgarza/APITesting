
from typing import List, Dict, Any, Union
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int) -> Union[Dict[str, Any], None]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate) -> Dict[str, Any]:
    new_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(new_user)
    db.commit()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Union[Dict[str, Any], None]:
    pass

def delete_user(db: Session, user_id: int) -> Union[Dict[str, Any], None]:
    pass

def get_post(db: Session, id: int) -> Union[Dict[str, Any], None]:
    pass

def get_posts(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict[str, Any]], None]:
    pass

def create_post(db: Session, owner_id: int, post: schemas.PostCreate) -> Dict[str, Any]:
    pass

def update_post(db: Session, id: int, post: schemas.PostUpdate) -> Union[Dict[str, Any], None]:
    pass

def delete_post(db: Session, id: int) -> Union[Dict[str, Any], None]:
    pass

def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> Union[List[Dict[str, Any]], None]:
    pass

def create_comment(db: Session, post_id: int, owner_id: int, comment: schemas.CommentCreate) -> Dict[str, Any]:
    pass

def update_comment(db: Session, id: int, comment: schemas.CommentUpdate) -> Union[Dict[str, Any], None]:
    pass

def delete_comment(db: Session, id: int) -> Union[Dict[str, Any], None]:
    pass
