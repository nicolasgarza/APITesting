from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"))  
    content = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User")
    post = relationship("Post", back_populates="comments",)
