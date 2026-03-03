from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db.sessions import create_db_and_tables, get_session
from app.models.cliente import Cliente # Solo para probar

app = FastAPI(title="Sistema de Gestión de Matafuegos")

# Al arrancar, crea las tablas si no existen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"mensaje": "Servidor de Matafuegos Online - Base de datos conectada"}

# Ejemplo de un endpoint para ver si funciona (luego lo pasaremos a otro archivo)
@app.get("/clientes")
def leer_clientes(session: Session = Depends(get_session)):
    # Aquí iría la lógica para traer clientes
    return {"status": "Listo para consultar clientes"}
