from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    comments = relationship("Comment", back_populates="owner", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
