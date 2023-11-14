from fastapi import APIRouter

router = APIRouter()

@router.get("/posts")
async def read_posts():
    return {"message": "List of all posts"}

@router.get("/posts/{post_id}")
async def read_post(post_id: int):
    return {"post_id": post_id, "title": "Example Post"}