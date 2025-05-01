from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    author: str
    read_time: Optional[str] = None
    published_at: Optional[datetime] = None

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostOut(BlogPostBase):
    id: int

    class Config:
        from_attributes = True