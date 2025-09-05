import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno")

motor = create_async_engine(
    DATABASE_URL,
    echo=True,  # Para ver las consultas SQL en desarrollo
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    motor, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """
    Dependency para obtener sesión de base de datos
    Esta función se usa como dependencia en los endpoints
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """Crear todas las tablas en la base de datos"""
    async with motor.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)