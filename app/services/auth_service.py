"""Authentication and user management service."""

from datetime import datetime, timedelta
import os
import jwt
import bcrypt
from typing import Optional

# In-memory user database (for development - replace with real DB in production)
USERS_DB = {}

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return username."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except jwt.InvalidTokenError:
        return None


def register_user(username: str, email: str, password: str) -> dict:
    """Register a new user."""
    if username in USERS_DB:
        raise ValueError("Username already exists")
    if any(user["email"].lower() == email.lower() for user in USERS_DB.values()):
        raise ValueError("Email already exists")
    
    USERS_DB[username] = {
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow()
    }
    
    return {"username": username, "email": email}


def authenticate_user(username_or_email: str, password: str) -> Optional[dict]:
    """Authenticate a user by username or email and return user info."""
    matched_username = None

    if username_or_email in USERS_DB:
        matched_username = username_or_email
    else:
        for username, user in USERS_DB.items():
            if user["email"].lower() == username_or_email.lower():
                matched_username = username
                break

    if matched_username is None:
        return None

    user = USERS_DB[matched_username]
    if not verify_password(password, user["password_hash"]):
        return None
    
    return {"username": matched_username, "email": user["email"]}


def get_user(username: str) -> Optional[dict]:
    """Get user by username."""
    if username not in USERS_DB:
        return None
    
    user = USERS_DB[username]
    return {"username": username, "email": user["email"]}
