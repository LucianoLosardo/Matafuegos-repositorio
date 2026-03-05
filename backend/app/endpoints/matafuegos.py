from fastapi import APIRouter
from app.db.sessions import create_db_and_tables, get_session, engine
from sqlmodel import Session, select
from app.models.matafuego import Matafuego

router = APIRouter(prefix="/matafuegos", 
                   tags=["matafuegos"],
                   responses={404: {"message": "No encontrado"}})

mataguegos_list = ["Matafuego 1","Matafuego 2","Matafuego 3"]


@router.get("/")
async def matafuegos():
    with Session(engine) as session:
        statement = select(Matafuego)
        # 2. Ejecutamos y traemos todos los resultados
        matafuegos = session.exec(statement).all()
    
        # 3. Lo imprimimos en la consola (opcional, para que lo veas vos)
        print("Matafuegos encontrados en DB:", matafuegos)
    
        return matafuegos
