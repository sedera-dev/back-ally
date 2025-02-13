from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from app.core.config import settings
from app.modules.auth.models.auth_model import UserInDB
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
# Configuration
SECRET_KEY = settings.SECRET_KEY 
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Configuration pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de données simulée
fake_users_db = {
    "sedera714": {
        "username": "sedera714",
        "email": "sederafanomezana@gmail.com",
        "full_name": "sedera fanomezana",
        "disabled": False,
        "hashed_password": pwd_context.hash("secret"),
    }
}

# Authentification OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token/")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour vérifier le token JWT
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username