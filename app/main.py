from fastapi import FastAPI

from app.routers import clientes
from app.routers import auth

app = FastAPI()

app.include_router(clientes.router)

app.include_router(auth.router)

@app.get("/")
def index():
    return {"message": "Zonora API is running"}