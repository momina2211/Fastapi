from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.Blog import schemas
from app.Blog.database import get_db
from app.Blog.repository import blog
from app.Blog import OAuth2

router = APIRouter(
    tags=["Blog"],
    prefix="/blog"
)

@router.post("/", response_model=schemas.BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(
    request: schemas.BlogBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user)
):
    return blog.create_blog(request, db, user_id=current_user.id)


@router.get("/", response_model=List[schemas.BlogResponse])
def get_all_blogs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    # current_user: schemas.UserResponse = Depends(OAuth2.get_current_user)
):
    return blog.get_all_blogs(skip=skip, limit=limit, db=db)


@router.get("/{blog_id}", response_model=schemas.BlogResponse)
def get_blog_by_id(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user)
):
    return blog.get_blog_by_id(blog_id, db)


@router.put("/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(
    blog_id: int,
    request: schemas.BlogBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user)
):
    blog_to_update = blog.get_blog_by_id(blog_id, db)
    if blog_to_update.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this blog"
        )
    return blog.update_blog(blog_id, request, db)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user)
):
    blog_to_delete = blog.get_blog_by_id(blog_id, db)
    if blog_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this blog"
        )
    blog.delete_blog(blog_id, db)
    return None
