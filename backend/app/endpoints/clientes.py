from fastapi import APIRouter
from app.db.sessions import create_db_and_tables, get_session, engine
from sqlmodel import Session, select
from app.models.cliente import Cliente

router = APIRouter(prefix="/clientes", 
                   tags=["clientes"],
                   responses={404: {"message": "No encontrado"}})


@router.get("/")
async def clientes():
    with Session(engine) as session:
        statement = select(Cliente)
        # 2. Ejecutamos y traemos todos los resultados
        clientes = session.exec(statement).all()
    
        # 3. Lo imprimimos en la consola (opcional, para que lo veas vos)
        print("Clientes encontrados en DB:", clientes)
    
        return clientes

