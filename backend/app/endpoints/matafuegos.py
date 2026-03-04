from fastapi import APIRouter

router = APIRouter(prefix="/matafuegos", 
                   tags=["matafuegos"],
                   responses={404: {"message": "No encontrado"}})

mataguegos_list = ["Matafuego 1","Matafuego 2","Matafuego 3"]


@router.get("/")
async def matafuegos():
    return mataguegos_list 
