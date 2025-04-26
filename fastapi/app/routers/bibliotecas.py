# fastapi/app/routers/bibliotecas.py
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
import uuid
# Importamos modelos desde app.models
from app.models import BibliotecaDimensional, BibliotecaDimensionalCreate

router = APIRouter(
    prefix="/bibliotecas", # Prefijo para todas las rutas en este archivo
    tags=["Bibliotecas Dimensionales"] # Agrupa en la documentación /docs
)

# "Base de datos" en memoria (solo para este ejemplo)
# En un proyecto real, interactuarías con una BD real aquí (quizás vía un archivo crud.py)
db_bibliotecas: Dict[str, BibliotecaDimensional] = {}

@router.post("/", response_model=BibliotecaDimensional, status_code=status.HTTP_201_CREATED)
async def crear_biblioteca(biblioteca_in: BibliotecaDimensionalCreate):
    """Crea una nueva Biblioteca Dimensional."""
    biblioteca_id = f"BIB-{uuid.uuid4()}"
    # Creamos una instancia del modelo completo (con ID) a partir del modelo de entrada
    nueva_biblioteca = BibliotecaDimensional(id_biblioteca=biblioteca_id, **biblioteca_in.model_dump())
    db_bibliotecas[biblioteca_id] = nueva_biblioteca # Guardamos en la 'DB'
    return nueva_biblioteca

@router.get("/", response_model=List[BibliotecaDimensional])
async def obtener_bibliotecas():
    """Obtiene una lista de todas las Bibliotecas Dimensionales."""
    return list(db_bibliotecas.values())

@router.get("/{biblioteca_id}", response_model=BibliotecaDimensional)
async def obtener_biblioteca_por_id(biblioteca_id: str):
    """Obtiene una Biblioteca Dimensional específica por su ID."""
    biblioteca = db_bibliotecas.get(biblioteca_id)
    if not biblioteca:
        # Si no se encuentra, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Biblioteca no encontrada")
    return biblioteca

# Aquí podrías añadir endpoints PUT (actualizar) y DELETE si los necesitas