from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db.sessions import create_db_and_tables, get_session
from app.endpoints import clientes, matafuegos

app = FastAPI(title="Sistema de Gestión de Matafuegos")

# Routers 

app.include_router(clientes.router)
app.include_router(matafuegos.router)

# Al arrancar, crea las tablas si no existen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"mensaje": "Servidor de Matafuegos Online - Base de datos conectada"}


