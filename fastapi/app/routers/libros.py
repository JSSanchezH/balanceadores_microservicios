# fastapi/app/routers/libros.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Optional
import uuid
# Importamos modelos desde app.models
from app.models import LibroPerdido, LibroPerdidoCreate
# Importamos la 'db' de bibliotecas para validar la clave foránea
from .bibliotecas import db_bibliotecas

router = APIRouter(
    prefix="/libros", # Prefijo para todas las rutas en este archivo
    tags=["Libros Perdidos"] # Agrupa en la documentación /docs
)

# "Base de datos" en memoria (solo para este ejemplo)
db_libros: Dict[str, LibroPerdido] = {}

@router.post("/", response_model=LibroPerdido, status_code=status.HTTP_201_CREATED)
async def crear_libro(libro_in: LibroPerdidoCreate):
    """
    Crea un nuevo Libro Perdido, asegurándose que su biblioteca de origen exista.
    """
    # --- Validación de la Clave Foránea (Importante para la relación) ---
    biblioteca_id_origen = libro_in.biblioteca_origen_id
    if biblioteca_id_origen not in db_bibliotecas:
        # Si la biblioteca referenciada NO existe, devuelve error 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La Biblioteca Dimensional de origen con ID '{biblioteca_id_origen}' no existe."
        )

    libro_id = f"LIB-{uuid.uuid4()}"
    # Creamos una instancia del modelo completo (con ID)
    nuevo_libro = LibroPerdido(id_libro=libro_id, **libro_in.model_dump())
    db_libros[libro_id] = nuevo_libro # Guardamos en la 'DB'
    return nuevo_libro

@router.get("/", response_model=List[LibroPerdido])
async def obtener_libros(
    # Parámetro de consulta opcional para filtrar
    biblioteca_id: Optional[str] = Query(None, description="Filtrar libros por el ID de su biblioteca de origen.")
    ):
    """
    Obtiene una lista de todos los Libros Perdidos.
    Permite filtrar por la biblioteca de origen usando el query parameter 'biblioteca_id'.
    """
    libros_lista = list(db_libros.values())

    # Si se proporciona el parámetro de filtro 'biblioteca_id'
    if biblioteca_id:
        # Opcional: Validar que la biblioteca usada para filtrar exista
        if biblioteca_id not in db_bibliotecas:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La Biblioteca Dimensional con ID '{biblioteca_id}' para filtrar no existe."
            )
        # Filtrar la lista
        libros_lista = [libro for libro in libros_lista if libro.biblioteca_origen_id == biblioteca_id]

    return libros_lista

@router.get("/{libro_id}", response_model=LibroPerdido)
async def obtener_libro_por_id(libro_id: str):
    """Obtiene un Libro Perdido específico por su ID."""
    libro = db_libros.get(libro_id)
    if not libro:
        # Si no se encuentra, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    return libro
