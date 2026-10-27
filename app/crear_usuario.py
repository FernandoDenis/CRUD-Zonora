from getpass import getpass
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Usuario
from app.security import hash_password


def main():
    nombre_usuario = input("Escribe tu nombre de usuario:").strip()
    
    password = getpass("Escribe tu contraseña:")
    
    password_confirmacion = getpass("Confirma tu contraseña:")
    
    if not nombre_usuario:
        print("Nombre de usuario vacio")
        return 
    
    if not password:
        print("Contraseña vacia")
        return
    
    if password != password_confirmacion:
        print("Contraseñas distintas")
        return
    
    with SessionLocal() as db:
        consulta = select(Usuario).where(Usuario.nombre_usuario == nombre_usuario)
        usuario_existente = db.scalar(consulta)
        
        if usuario_existente:
            print("El nombre de usuario ya existe")
            return
        
        password_hash = hash_password(password)
        
        usuario = Usuario(nombre_usuario=nombre_usuario, password_hash=password_hash)
        
        db.add(usuario)
        db.commit()
        print("Usuario creado correctamente")
        
if __name__ == "__main__":
    main()
