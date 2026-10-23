from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.schemas import ClienteCreate, ClienteRead, ClienteUpdate
from app.models import Cliente


router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.post("", response_model=ClienteRead, status_code=201)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    cliente = Cliente(nombre=datos.nombre)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.get("/{cliente_id}", response_model=ClienteRead, status_code=200)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
    
@router.get("", response_model=list[ClienteRead], status_code=200)
def listar_clientes(db: Session = Depends(get_db)):
    consulta = select(Cliente)
    resultado = db.scalars(consulta)
    clientes = resultado.all()
    return clientes

@router.patch("/{cliente_id}", response_model=ClienteRead, status_code=200)
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente.nombre = datos.nombre
    db.commit()
    db.refresh(cliente)
    return cliente
