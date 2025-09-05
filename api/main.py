from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import encuesta_laboral_salud_mental
from api.database.conexion import motor, create_tables
import asyncio

async def lifespan(app: FastAPI):
    """Manejador de ciclo de vida de la aplicación"""
    # Evento de inicio
    await create_tables()
    yield
    # Evento de cierre (liberar recursos aquí)

api = FastAPI(
    title="API Encuestas - Acercándote.org",
    description="API para registro de encuestas y análisis de datos",
    version="1.0.0",
    lifespan=lifespan
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(encuesta_laboral_salud_mental.router, prefix="/api/v1")


@api.get("/")
async def root():
    """Endpoint de salud para verificar que la API está funcionando"""
    return {
        "message": "API Encuestas - Acercándote.org", 
        "status": "active",
        "version": "1.0.0"
    }


@api.get("/estado")
async def health_check():
    """Endpoint de health check para monitoreo"""
    return {"status": "Sistema funcionando correctamente"}