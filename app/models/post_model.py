from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
