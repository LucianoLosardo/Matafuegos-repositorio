from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
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
async def obtener_tabla_matafuegos(
    request: Request, 
    mes_busqueda: Optional[str] = None,
    nombre_cliente: Optional[str] = None,
    session: Session = Depends(get_session)
):

    query = select(Matafuego, Cliente).join(Cliente)
    
    if mes_busqueda:
        año_str, mes_str = mes_busqueda.split("-")
        año_objetivo = int(año_str)
        mes_objetivo = int(mes_str)
        
        año_recarga = año_objetivo - 1
        _, ultimo_dia = calendar.monthrange(año_recarga, mes_objetivo)
        fecha_limite = date(año_recarga, mes_objetivo, ultimo_dia)
        
        query = query.where(Matafuego.fecha_ultima_recarga <= fecha_limite)

    if nombre_cliente:
        # .ilike() ignora si lo escribiste en mayúscula o minúscula. ¡Es mucho más seguro!
        query = query.where(Cliente.nombre.ilike(f"%{nombre_cliente}%"))

    resultados_db = session.exec(query).all()
    

    return templates.TemplateResponse(
        "lista_matafuegos.html", 
        {"request": request, "resultados": resultados_db}
    )

@router.post("/")
async def crear_matafuego(
    # Atajamos cada campo del formulario indicando que viene de un Form()
    numero_serie: str = Form(...),
    tipo: str = Form(...),
    capacidad: str = Form(...),
    fecha_ultima_recarga: date = Form(...),
    anio_matafuego: int = Form(...),
    id_cliente: int = Form(...),
    session: Session = Depends(get_session)
):
    try:
        # 1. Armamos el objeto con los datos que nos mandó HTMX
        nuevo_matafuego = Matafuego(
            numero_serie=numero_serie,
            tipo=tipo,
            capacidad=capacidad,
            fecha_ultima_recarga=fecha_ultima_recarga,
            anio_matafuego=anio_matafuego,
            id_cliente=id_cliente
        )
        
        # 2. Lo preparamos y lo guardamos en la base de datos
        session.add(nuevo_matafuego)
        session.commit()
        
        # 3. Devolvemos un pedacito de HTML con un mensaje de éxito
        # Esto es lo que HTMX va a inyectar al lado del botón
        return HTMLResponse(
            content="<span class='text-green-600 font-semibold'>✅ ¡Guardado con éxito!</span>",
             headers={"HX-Trigger": "matafuego-guardado"}
        )
        
    except Exception as e:
        # Si algo falla (ej: el id_cliente no existe), devolvemos un error en rojo
        print(f"Error al guardar: {e}")
        return HTMLResponse(
            content="<span class='text-red-600 font-semibold'>❌ Error al guardar. Verifica el ID del cliente.</span>"
        )
    

@router.delete("/{matafuego_id}", response_class=HTMLResponse)
async def borrar_matafuego(matafuego_id: int, session: Session = Depends(get_session)):
    # Buscamos el cliente en la base de datos
    matafuego_a_borrar = session.get(Matafuego, matafuego_id)
    
    # Si por alguna razón no existe, tiramos un error 404
    if not matafuego_a_borrar:
        raise HTTPException(status_code=404, detail="Matafuego no encontrado")
    
    # Lo borramos y guardamos los cambios
    session.delete(matafuego_a_borrar)
    session.commit()
    
    return ""