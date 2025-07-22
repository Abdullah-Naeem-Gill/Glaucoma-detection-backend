from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# JWT configuration
SECRET_KEY = "supersecretkey"  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# Token validation with role checking
bearer_scheme = HTTPBearer()

def verify_role(is_doctor: bool = False, is_patient: bool = False):
    def role_dependency(token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
        payload = decode_access_token(token.credentials)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        
        role = payload.get("role")
        if role not in ("doctor", "patient"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role in token")
        
        if is_doctor and role != "doctor":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Doctors only")
        if is_patient and role != "patient":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Patients only")
        
        return payload
    return role_dependency
