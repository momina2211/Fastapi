from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.Blog.database import get_db
from app.Blog import models
from app.Blog.hashing import verify_password  # Assuming verify_password is standalone
from app.Blog.token import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials'
        )

    if not verify_password(request.password, user.password):  # Corrected the function call
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid password'
        )

    # Include both 'sub' (email) and 'id' in the payload
    access_token = create_access_token(data={"sub": user.email, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
