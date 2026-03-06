from fastapi import APIRouter, Request
from app.db.sessions import create_db_and_tables, get_session, engine
from sqlmodel import Session, select
from app.models.matafuego import Matafuego
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/matafuegos", 
                   tags=["matafuegos"],
                   responses={404: {"message": "No encontrado"}})

templates = Jinja2Templates(directory="app/templates/matafuegos")

@router.get("/")
async def matafuegos():
    with Session(engine) as session:
        statement = select(Matafuego)
        # 2. Ejecutamos y traemos todos los resultados
        matafuegos = session.exec(statement).all()
    
        # 3. Lo imprimimos en la consola 
        print("Matafuegos encontrados en DB:", matafuegos)
    
        return matafuegos

@router.get("/tabla")
async def obtener_matafuegos(request: Request):
    with Session(engine) as session:
        statement = select(Matafuego)
        # Ejecutamos y traemos todos los resultados
        matafuegos = session.exec(statement).all()
        # Renderizamos el HTML inyectando la variable "matafuegos"
        return templates.TemplateResponse(
            "lista_matafuegos.html", 
            {"request": request, "matafuegos": matafuegos}
        )