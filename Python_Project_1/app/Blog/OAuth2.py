from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.Blog.token import verify_token


# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to retrieve the current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Extract and validate the current user from the JWT.

    Args:
        token (str): Bearer token extracted by OAuth2PasswordBearer.

    Returns:
        schemas.TokenData: Token data containing user email.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
