# File: routers/blog.py

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from models.blog import BlogPost  # Tortoise model
from schemas.blog import BlogPostCreate, BlogPostOut
from typing import List

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.post("/posts", response_model=BlogPostOut)
async def create_post(data: BlogPostCreate):
    post = await BlogPost.create(**data.dict())
    return await BlogPostOut.from_tortoise_orm(post)


@router.get("/posts", response_model=List[BlogPostOut])
async def get_posts():
    posts = await BlogPost.all().order_by("-published_at")
    return [await BlogPostOut.from_tortoise_orm(post) for post in posts]


@router.get("/posts/{slug}", response_model=BlogPostOut, responses={404: {"model": HTTPNotFoundError}})
async def get_post(slug: str):
    post = await BlogPost.get_or_none(slug=slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await BlogPostOut.from_tortoise_orm(post)
