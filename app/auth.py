from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
import jwt
from jwt.exceptions import InvalidTokenError

from app.config import settings
from app.database import get_db
from app.models import Usuario
from app.security import verify_password

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme), db: Session = Depends(get_db)) -> Usuario:
    
    if not credentials:
        raise HTTPException(status_code=401, detail="No autenticado", headers={"WWW-Authenticate": "Bearer"})
    
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm], options={"require": ["sub", "exp"]})
        usuario_id = int(payload["sub"])
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Token invalido o vencido", headers={"WWW-Authenticate": "Bearer"} )
    
    usuario = db.get(Usuario, usuario_id)
    
    if not usuario:
        raise HTTPException(status_code=401, detail="No autenticado", headers={"WWW-Authenticate": "Bearer"})
    
    return usuario
    

def autenticar_usuario(db: Session, nombre_usuario: str, password: str) -> Usuario | None:
    consulta = select(Usuario).where(Usuario.nombre_usuario == nombre_usuario)
    usuario = db.scalar(consulta)
    
    if not usuario:
        return None
    
    validacion = verify_password(password, usuario.password_hash)
    
    if not validacion:
        return None
    
    return usuario
    