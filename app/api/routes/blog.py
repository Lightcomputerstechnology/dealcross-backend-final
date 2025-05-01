File: app/api/routes/blog.py

from fastapi import APIRouter, HTTPException, Depends from sqlalchemy.orm import Session from core.database import get_db from models.blog import BlogPost from schemas.blog import BlogPostOut

router = APIRouter(prefix="/blog", tags=["Blog"])

=== Get all blog posts ===

@router.get("/posts", response_model=list[BlogPostOut]) def get_all_blog_posts(db: Session = Depends(get_db)): posts = db.query(BlogPost).order_by(BlogPost.published_at.desc()).all() return posts

=== Get blog post by slug ===

@router.get("/posts/{slug}", response_model=BlogPostOut) def get_post_by_slug(slug: str, db: Session = Depends(get_db)): post = db.query(BlogPost).filter(BlogPost.slug == slug).first() if not post: raise HTTPException(status_code=404, detail="Blog post not found") return post

