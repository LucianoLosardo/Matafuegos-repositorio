from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from app.db.sessions import create_db_and_tables, get_session, engine
from sqlmodel import Session, select
from app.models.cliente import Cliente
from fastapi.templating import Jinja2Templates
from typing import Optional
import re

router = APIRouter(prefix="/clientes", 
                   tags=["clientes"],
                   responses={404: {"message": "No encontrado"}})

templates = Jinja2Templates(directory="app/templates/clientes")

@router.get("/")
async def clientes(request: Request):
    return templates.TemplateResponse("index_cliente.html", {"request": request})
        

@router.get("/tabla")
async def obtener_clientes(
    request: Request,
    nombre_busqueda: Optional[str] = None,
    session: Session = Depends(get_session)
):

    query = select(Cliente)

    if nombre_busqueda:
       query = query.where(Cliente.nombre.icontains(nombre_busqueda))
    
    clientes = session.exec(query).all()

    # Renderizamos el HTML inyectando la variable "clientes"
    return templates.TemplateResponse(
        "lista_clientes.html", 
        {"request": request, "clientes": clientes}
    )

@router.post("/", response_class=HTMLResponse)
def crear_cliente(
    # Recibimos los datos exactos que manda el atributo "name" del HTML
    nombre: str = Form(...), # Los tres puntitos significan que es obligatorio
    dni: str | None = Form(None),
    email: str | None = Form(None),
    telefono: str | None = Form(None),
    direccion: str | None = Form(None),
    session: Session = Depends(get_session)
):
  # --- VALIDACIONES ---
    
    # Validar Email 
    if email:
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            return """
            <div class="p-2 bg-red-100 text-red-700 border border-red-400 rounded">
                ❌ Error: El formato del email no es válido.
            </div>
            """

    # Validar DNI 
    if dni:
        if not dni.isdigit():
            return """
            <div class="p-2 bg-red-100 text-red-700 border border-red-400 rounded">
                ❌ Error: El DNI debe contener solo números.
            </div>
            """
            
        # Validar que el DNI no exista ya en la base de datos
        cliente_existente = session.exec(select(Cliente).where(Cliente.dni == dni)).first()
        if cliente_existente:
            return f"""
            <div class="p-2 bg-red-100 text-red-700 border border-red-400 rounded">
                ❌ Error: Ya existe un cliente con el DNI {dni}.
            </div>
            """

    # --- SI TODO ESTÁ BIEN, GUARDAMOS ---
    nuevo_cliente = Cliente(
        nombre=nombre, dni=dni, email=email, telefono=telefono, direccion=direccion
    )
    
    session.add(nuevo_cliente)
    session.commit()
    
    # Cartel de éxito
    return f"""
    <div class="p-2 bg-green-100 text-green-700 border border-green-400 rounded">
        ✅ ¡Cliente <strong>{nuevo_cliente.nombre}</strong> guardado con éxito!
    </div>
    """