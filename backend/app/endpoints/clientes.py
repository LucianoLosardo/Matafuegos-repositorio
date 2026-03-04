from fastapi import APIRouter

router = APIRouter(prefix="/clientes", 
                   tags=["clientes"],
                   responses={404: {"message": "No encontrado"}})

client_list = ["Cliente 1", "Cliente 2", "Cliente 3"]

@router.get("/")
async def clientes():
    return client_list