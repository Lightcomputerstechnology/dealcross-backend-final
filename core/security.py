from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Constants
SECRET_KEY = "your-very-secure-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create JWT Token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)
