import os
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Generator

# 1. URL de conexión (tomada de las variables de entorno de tu Docker Compose)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user_matafuegos:password_segura@db:5432/db_matafuegos"
)

# 2. El motor (Engine) que habla con Postgres
# echo=True es genial en desarrollo para ver las consultas SQL en la terminal
engine = create_engine(DATABASE_URL, echo=True)

# 3. Función para crear las tablas (se llama al iniciar la app)
def create_db_and_tables():
    # IMPORTANTE: Importamos los modelos aquí para que SQLModel los registre
    from app.models.cliente import Cliente
    from app.models.matafuego import Matafuego
    
    SQLModel.metadata.create_all(engine)

# 4. Dependencia para los Endpoints (abre una sesión y la cierra al terminar)
def get_session() -> Generator:
    with Session(engine) as session:
        yield session