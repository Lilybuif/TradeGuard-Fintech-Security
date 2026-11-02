from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone

# Password hashing context using bcrypt
pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "tradeguard_super_secret_jwt_key_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt."""
    return pw_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against the stored hash."""
    return pw_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Generates a signed JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt