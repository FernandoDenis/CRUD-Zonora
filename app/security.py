from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)

def create_access_token(usuario_id: int) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    payload = {
        "sub": str(usuario_id),
        "exp": expiration
    }
    
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    