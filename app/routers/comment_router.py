from fastapi import APIRouter

router = APIRouter()

@router.get("/comments")
async def read_comments():
    return {"message": "List of all comments"}

@router.get("/comments/{comment_id}")
async def read_comment(comment_id: int):
    return {"comment_id": comment_id, "content": "Example Comment"}