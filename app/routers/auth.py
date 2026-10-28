from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import autenticar_usuario
from app.security import create_access_token
from app.schemas import LoginRequest, TokenResponse


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, datos.nombre_usuario, datos.password)
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_access_token(usuario.id)
    
    return TokenResponse(access_token=token, token_type="bearer")