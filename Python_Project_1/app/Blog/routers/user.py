from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.Blog import schemas, OAuth2
from app.Blog.database import get_db
from app.Blog.repository import user

router = APIRouter(
    tags=["User"],
    prefix="/user"
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user),
):
    return user.create(request, db)


@router.get("/", response_model=List[schemas.UserResponse])
def all_user(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user),
):
    return user.all_users(db)


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user),
):
    return user.get_user_by_id(user_id, db)


@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    request: schemas.UserBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user),
):
    return user.update(user_id, request, db)


@router.delete("/{user_id}", response_model=schemas.UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(OAuth2.get_current_user),
):
    return user.delete(user_id, db)
