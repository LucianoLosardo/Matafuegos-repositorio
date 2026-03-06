from fastapi import APIRouter, Request
from app.db.sessions import create_db_and_tables, get_session, engine
from sqlmodel import Session, select
from app.models.cliente import Cliente
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/clientes", 
                   tags=["clientes"],
                   responses={404: {"message": "No encontrado"}})

templates = Jinja2Templates(directory="app/templates/clientes")

@router.get("/")
async def clientes():
    with Session(engine) as session:
        statement = select(Cliente)
        # 2. Ejecutamos y traemos todos los resultados
        clientes = session.exec(statement).all()
    
        # 3. Lo imprimimos en la consola (opcional, para que lo veas vos)
        print("Clientes encontrados en DB:", clientes)
    
        return clientes

@router.get("/tabla")
async def obtener_clientes(request: Request):
    with Session(engine) as session:
        statement = select(Cliente)
        # Ejecutamos y traemos todos los resultados
        clientes = session.exec(statement).all()
        # Renderizamos el HTML inyectando la variable "clientes"
        return templates.TemplateResponse(
            "lista.html", 
            {"request": request, "clientes": clientes}
        )
