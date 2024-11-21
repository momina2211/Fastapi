from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException
from app.Blog import schemas

# Secret key and algorithm for JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token with optional expiration time.

    Args:
        data (dict): The payload to include in the token. This should include `id` and `email`.
        expires_delta (timedelta | None): Custom expiration time. Default is 15 minutes.

    Returns:
        str: Encoded JWT.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Ensure `id` and `email` are in the payload
    if 'id' not in to_encode or 'sub' not in to_encode:
        raise ValueError("Token data must include 'id' and 'sub' (email).")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException):
    """
    Verify the given JWT token and extract user data.

    Args:
        token (str): The JWT to verify.
        credentials_exception (HTTPException): Exception to raise if the token is invalid.

    Returns:
        schemas.TokenData: An object containing the token's email and id fields.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded token payload:", payload)  # Debugging
        email: str = payload.get("sub")
        user_id: int = payload.get("id")  # Extract 'id' from the token payload

        if email is None or user_id is None:
            print("Missing required fields in token payload")
            raise credentials_exception

        print("Email:", email, "User ID:", user_id)  # Debugging
        return schemas.TokenData(email=email, id=user_id)
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise credentials_exception
    except jwt.InvalidTokenError:
        print("Invalid token")
        raise credentials_exception




