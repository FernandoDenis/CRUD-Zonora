from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ClienteCreate, ClienteRead
from app.models import Cliente


router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.post("", response_model=ClienteRead, status_code=201)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    cliente = Cliente(nombre=datos.nombre)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente