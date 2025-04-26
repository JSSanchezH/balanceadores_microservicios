# fastapi/app/main.py
from fastapi import FastAPI
# Importamos los routers definidos en la carpeta 'routers'
from .routers import bibliotecas, libros # Usamos '.' porque están en el mismo paquete 'app'

# Define los metadatos para los tags (opcional, mejora /docs)
tags_metadata = [
    {
        "name": "Bibliotecas Dimensionales",
        "description": "Operaciones con Bibliotecas Dimensionales. Cada una es única y existe en un plano diferente.",
    },
    {
        "name": "Libros Perdidos",
        "description": "Operaciones con Libros Perdidos. Libros extraviados de sus bibliotecas originales.",
    },
    {
        "name": "Root",
        "description": "Endpoint raíz de la API."
    }
]

# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="Archivo de Bibliotecas Dimensionales y Libros Perdidos",
    description="API para catalogar bibliotecas interdimensionales y los libros perdidos de ellas.",
    version="0.1.0",
    openapi_tags=tags_metadata # Usa los metadatos definidos arriba
)

# Incluye los routers en la aplicación principal
# Todas las rutas definidas en bibliotecas.router tendrán el prefijo /bibliotecas
app.include_router(bibliotecas.router)
# Todas las rutas definidas en libros.router tendrán el prefijo /libros
app.include_router(libros.router)

@app.get("/", tags=["Root"])
async def read_root():
    """Endpoint raíz de bienvenida."""
    # Nota: Este endpoint no tendrá prefijo
    return {"mensaje": "Bienvenido al Archivo de Bibliotecas Dimensionales y Libros Perdidos"}
