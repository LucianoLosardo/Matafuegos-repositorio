from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db.sessions import create_db_and_tables, get_session, engine
from app.endpoints import clientes, matafuegos
from datetime import date
from app.models.cliente import Cliente
from app.models.matafuego import Matafuego

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

@app.get("/test-db")
def test_db(session: Session = Depends(get_session)):
    crear_datos_ejemplo(session)
    return {"status": "Datos cargados correctamente"} 



def crear_datos_ejemplo(session: Session):
    # 1. Creamos el objeto Cliente
    nuevo_cliente = Cliente(
        nombre="Luciano Ingenieria",
        dni="20400500",
        direccion="Av. Siempre Viva 742",
        email="luciano@ejemplo.com",
        telefono="1122334455"
    )

    with Session(engine) as session:  
        session.add(nuevo_cliente)  

        session.commit()  