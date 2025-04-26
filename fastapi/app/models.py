# fastapi/app/models.py
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

# --- Modelo para Biblioteca Dimensional ---

class BibliotecaDimensionalBase(BaseModel):
    nombre: str = Field(..., example="La Biblioteca Silente")
    plano_existencia: str = Field(..., example="Plano Astral")
    descripcion: Optional[str] = Field(None, example="Solo accesible en sueños profundos.")
    arquitectura_dominante: Optional[str] = Field(None, example="Cristal y Niebla")

class BibliotecaDimensionalCreate(BibliotecaDimensionalBase):
    pass

class BibliotecaDimensional(BibliotecaDimensionalBase):
    id_biblioteca: str = Field(..., example=f"BIB-{uuid.uuid4()}")

    class Config:
        from_attributes = True

# --- Modelo para Libro Perdido ---

class LibroPerdidoBase(BaseModel):
    titulo: str = Field(..., example="El Tomo de las Estrellas Olvidadas")
    autor_aparente: Optional[str] = Field("Desconocido", example="El Escriba Ciego")
    descripcion_cubierta: Optional[str] = Field(None, example="Cuero negro sin marcas, frío al tacto.")
    # --- Clave Foránea (Relación) ---
    biblioteca_origen_id: str = Field(..., example="BIB-...") # Debe ser un ID de BibliotecaDimensional existente

class LibroPerdidoCreate(LibroPerdidoBase):
    pass

class LibroPerdido(LibroPerdidoBase):
    id_libro: str = Field(..., example=f"LIB-{uuid.uuid4()}")

    class Config:
        from_attributes = True