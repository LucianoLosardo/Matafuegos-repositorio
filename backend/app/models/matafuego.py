from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from .cliente import Cliente

class Matafuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_serie: str = Field(index=True, unique=True)
    tipo: str              # ABC, CO2, etc.
    capacidad: str         # 1kg, 5kg, etc.
    fecha_ultima_recarga: date 
    anio_matafuego: int    
    
    # Relación con el Cliente (Obligatorio)
    id_cliente: int = Field(foreign_key="cliente.id") 
    cliente: Optional["Cliente"] = Relationship(back_populates="matafuegos")