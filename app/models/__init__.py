from .base import Base  # Import base declarative class
from .user_model import User
from .post_model import Post
from .comment_model import Comment

# Optionally, you can define a function to create all tables
def create_tables(engine):
    Base.metadata.create_all(bind=engine)
