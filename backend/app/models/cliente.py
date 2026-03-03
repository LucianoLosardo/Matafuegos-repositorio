from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING

# Esto evita errores de importación circular al definir la relación
if TYPE_CHECKING:
    from .matafuego import Matafuego

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    dni: str = Field(index=True, unique=True)
    
    # Atributos Opcionales
    direccion: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    telefono: Optional[str] = Field(default=None)
    
    # Relación: Un cliente tiene muchos matafuegos
    matafuegos: List["Matafuego"] = Relationship(back_populates="cliente")