from fastapi import FastAPI
from app.routers import post_router, user_router, comment_router

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
app.include_router(comment_router)
