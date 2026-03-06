from fastapi import APIRouter, Request, Depends
from app.db.sessions import create_db_and_tables, get_session, engine
from sqlmodel import Session, select
from app.models.matafuego import Matafuego
from app.models.cliente import Cliente
from fastapi.templating import Jinja2Templates
from datetime import date
from typing import Optional
import calendar

router = APIRouter(prefix="/matafuegos", 
                   tags=["matafuegos"],
                   responses={404: {"message": "No encontrado"}})

templates = Jinja2Templates(directory="app/templates/matafuegos")

#@router.get("/")
async def matafuegos():
    with Session(engine) as session:
        statement = select(Matafuego)
        # 2. Ejecutamos y traemos todos los resultados
        matafuegos = session.exec(statement).all()
    
        # 3. Lo imprimimos en la consola 
        print("Matafuegos encontrados en DB:", matafuegos)
    
        return matafuegos

@router.get("/")
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
    

@router.get("/tabla")
def obtener_tabla_matafuegos(
    request: Request, 
    mes_busqueda: Optional[str] = None,
    session: Session = Depends(get_session)
):
    # 1. LA MAGIA DEL JOIN: Pedimos ambas tablas y le decimos que las cruce
    query = select(Matafuego, Cliente).join(Cliente)
    
    if mes_busqueda:
        año_str, mes_str = mes_busqueda.split("-")
        año_objetivo = int(año_str)
        mes_objetivo = int(mes_str)
        
        año_recarga = año_objetivo - 1
        _, ultimo_dia = calendar.monthrange(año_recarga, mes_objetivo)
        fecha_limite = date(año_recarga, mes_objetivo, ultimo_dia)
        
        query = query.where(Matafuego.fecha_ultima_recarga <= fecha_limite)

    # 2. Resultados: Esto ahora devuelve una lista de parejas (tuplas): 
    # [(matafuego1, cliente1), (matafuego2, cliente2)...]
    resultados_db = session.exec(query).all()
    
    # 3. Le pasamos esos "resultados" a la plantilla
    return templates.TemplateResponse(
        "lista_matafuegos.html", 
        {"request": request, "resultados": resultados_db}
    )