from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    username: Optional[str] = None
