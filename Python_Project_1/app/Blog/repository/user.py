from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.Blog import models, schemas
from app.Blog.hashing import get_password_hash


def create(request: schemas.UserCreate, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=get_password_hash(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def all_users(db: Session):
    users = db.query(models.User).all()
    return users


def get_user_by_id(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def update(user_id: int, request: schemas.UserBase, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if request.name:
        user.name = request.name
    if request.email:
        user.email = request.email
    if request.password:
        user.password = get_password_hash(request.password)

    db.commit()
    return user


def delete(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()
    return user
