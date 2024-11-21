from sqlalchemy.orm import Session
from app.Blog import models, schemas
from fastapi import HTTPException, status


def create_blog(request: schemas.BlogBase, db: Session, user_id: int):
    new_blog = models.Blog(title=request.title, description=request.description, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all_blogs(skip: int, limit: int, db: Session):
    return db.query(models.Blog).offset(skip).limit(limit).all()


def get_blog_by_id(blog_id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    return blog


def update_blog(blog_id: int, request: schemas.BlogBase, db: Session):
    blog = get_blog_by_id(blog_id, db)
    blog.title = request.title
    blog.description = request.description
    db.commit()
    db.refresh(blog)
    return blog


def delete_blog(blog_id: int, db: Session):
    blog = get_blog_by_id(blog_id, db)
    db.delete(blog)
    db.commit()
