from fastapi import FastAPI, Depends, Request
from sqlmodel import Session
from app.db.sessions import create_db_and_tables, get_session, engine
from app.endpoints import clientes, matafuegos
from datetime import date
from app.models.cliente import Cliente
from app.models.matafuego import Matafuego
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # Para el CSS después

app = FastAPI(title="Sistema de Gestión de Matafuegos")

# Configuramos las plantillas
templates = Jinja2Templates(directory="app/templates")

# Routers 

app.include_router(clientes.router)
app.include_router(matafuegos.router)

# Al arrancar, crea las tablas si no existen
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/test-db")
def test_db(session: Session = Depends(get_session)):
    crear_datos_ejemplo(session)
    return {"status": "Datos cargados correctamente"} 



def crear_datos_ejemplo(session: Session):
    nuevo_matafuego = Matafuego(
        numero_serie="SERIE-123",
        tipo="ABC",
        capacidad="5kg",
        fecha_ultima_recarga=date.today(),
        anio_matafuego=2024,
        id_cliente=1
    )

    with Session(engine) as session:  
        session.add(nuevo_matafuego)  

        session.commit()  