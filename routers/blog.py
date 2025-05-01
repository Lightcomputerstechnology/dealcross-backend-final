from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.blog import BlogPost
from schemas.blog import BlogPostCreate, BlogPostOut
from typing import List

router = APIRouter(prefix="/blog", tags=["Blog"])

@router.post("/posts", response_model=BlogPostOut)
def create_post(data: BlogPostCreate, db: Session = Depends(get_db)):
    post = BlogPost(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/posts", response_model=List[BlogPostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(BlogPost).order_by(BlogPost.published_at.desc()).all()

@router.get("/posts/{slug}", response_model=BlogPostOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post