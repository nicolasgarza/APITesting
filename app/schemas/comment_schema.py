from pydantic import BaseModel

class CommentBase(BaseModel):
    body: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    owner_id: int

    class Config:
        orm_mode = True 

class CommentUpdate(CommentBase):
    body: str