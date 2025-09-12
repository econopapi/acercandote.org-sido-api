import traceback
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from api.database.conexion import get_db
from api.modelos.encuesta_laboral_salud_mental import EncuestaLaboralSaludMental, EstadosMexico, MunicipiosMexico, RolesOrganizacion
from api.schemas.encuesta_laboral_salud_mental import EncuestaCreate, EncuestaResponse, EncuestaListResponse
from api.servicios.encuesta_laboral_salud_mental import EncuestaService

router = APIRouter(
    prefix="/encuestas/laboral-salud-mental",
    tags=["Encuestas de Salud Mental Laboral"],
    responses={404: {"description": "No encontrado"}}
)


def get_encuesta_service() -> EncuestaService:
    """Dependency injection para el servicio de encuestas"""
    return EncuestaService()


# Endpoints para obtener las preguntas desde db para el frontend

#obtener estados
@router.get("/preguntas/estados-mexico",
            summary="Obtener lista de estados de México",
            description="Devuelve una lista de estados para el campo de selección en la encuesta")
async def obtener_estados_mexico(db: AsyncSession = Depends(get_db)) -> List[str]:
    result = await db.execute(select(EstadosMexico.id_estado, EstadosMexico.nombre_estado).order_by(EstadosMexico.nombre_estado))
    estados = [{
            "id": row[0],
            "nombre": row[1]}
        for row in result.fetchall()]
    return JSONResponse(content={"estados": estados})


#obtener municipios por estado
@router.get("/preguntas/municipios-mexico",
            summary="Obtener lista de municipios de México por estado",
            description="Devuelve una lista de municipios para el campo de selección en la encuesta, filtrado por estado")
async def obtener_municipios_mexico(estado: int = Query(..., ge=1, description="ID del estado"),
                                    db: AsyncSession = Depends(get_db)) -> List[str]:
    result = await db.execute(select(MunicipiosMexico.id_municipio, MunicipiosMexico.nombre_municipio).where(MunicipiosMexico.id_estado == estado).order_by(MunicipiosMexico.nombre_municipio))
    municipios = [{
            "id": row[0],
            "nombre": row[1]}
        for row in result.fetchall()]
    
    print(f"Municipios encontrados para estado {estado}: {len(municipios)}")  # Debug log
    
    return JSONResponse(content={"municipios": municipios})


#obtener roles organizacion
@router.get("/preguntas/roles-organizacion",
            summary="Obtener lista de roles dentro de una organización",
            description="Devuelve una lista de roles para el campo de selección en la encuesta")
async def obtener_roles_organizacion(db: AsyncSession = Depends(get_db)) -> List[str]:
    result = await db.execute(select(RolesOrganizacion.id_rol_organizacion, RolesOrganizacion.nombre_rol).order_by(RolesOrganizacion.nombre_rol))
    roles = [{
            "id": row[0],
            "nombre": row[1]}
        for row in result.fetchall()]
    return JSONResponse(content={"roles": roles})



@router.get("/", summary="Endpoint de prueba", description="Verifica que el router de encuestas está activo")
async def prueba_encuesta():
    return {"message": "Router de encuestas de salud mental laboral activo"}


@router.post(
    "/respuestas",
    response_model=EncuestaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva respuesta de encuesta",
    description="Crea un nuevo registro de encuesta de salud mental laboral con todas las respuestas del participante"
)
async def crear_respuesta_encuesta(
    encuesta_data: EncuestaCreate,
    db: AsyncSession = Depends(get_db),
    encuesta_service: EncuestaService = Depends(get_encuesta_service)
):
    """
    Endpoint principal para registrar una nueva respuesta de encuesta.
    
    Recibe todos los datos de la encuesta en formato JSON y los guarda
    en la base de datos con validaciones automáticas.
    
    Args:
        encuesta_data: Datos de la encuesta validados por Pydantic
        db: Sesión de base de datos (inyección de dependencia)
        encuesta_service: Servicio de lógica de negocio
        
    Returns:
        EncuestaResponse: Datos de la encuesta creada con ID y metadatos
        
    Raises:
        HTTPException: Si hay errores de validación o problemas en la base de datos
    """
    try:
        # Usar el servicio para crear la encuesta
        nueva_encuesta = await encuesta_service.crear_encuesta(db, encuesta_data)
        
        return nueva_encuesta
        
    except ValueError as e:
        # Capturar el rastreo completo del error
        error_trace = traceback.format_exc()
        print(f"ValueError: {error_trace}")  # Log en la terminal para depuración
        
        # Respuesta HTTP con detalles adicionales
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Error de validación",
                "message": str(e),
                "trace": error_trace.splitlines()[-1]  # Última línea del rastreo
            }
        )
    except Exception as e:
        # Capturar el rastreo completo del error
        error_trace = traceback.format_exc()
        print(f"Exception: {error_trace}")  # Log en la terminal para depuración
        
        # Respuesta HTTP con detalles adicionales
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Error interno del servidor",
                "message": str(e),
                "trace": error_trace.splitlines()[-1]  # Última línea del rastreo
            }
        )


@router.get(
    "/respuestas",
    response_model=EncuestaListResponse,
    summary="Listar respuestas de encuestas",
    description="Obtiene una lista paginada de respuestas de encuestas con filtros opcionales"
)
async def listar_respuestas_encuestas(
    # Parámetros de paginación
    pagina: int = Query(1, ge=1, description="Número de página (comenzando desde 1)"),
    tamanio_pagina: int = Query(10, ge=1, le=100, description="Cantidad de registros por página"),
    
    # Filtros opcionales
    id_organizacion: Optional[int] = Query(None, description="Filtrar por ID de organización"),
    edad_minima: Optional[int] = Query(None, ge=18, description="Edad mínima del encuestado"),
    edad_maxima: Optional[int] = Query(None, le=100, description="Edad máxima del encuestado"),
    
    # Dependencias
    db: AsyncSession = Depends(get_db),
    encuesta_service: EncuestaService = Depends(get_encuesta_service)
):
    """
    Lista las respuestas de encuestas con paginación y filtros opcionales.
    
    Permite filtrar por organización y rango de edades, y paginar los resultados
    para manejar grandes volúmenes de datos de manera eficiente.
    
    Args:
        pagina: Número de página a obtener
        tamanio_pagina: Cantidad de registros por página
        id_organizacion: Filtro opcional por organización
        edad_minima: Filtro opcional por edad mínima
        edad_maxima: Filtro opcional por edad máxima
        db: Sesión de base de datos
        encuesta_service: Servicio de lógica de negocio
        
    Returns:
        EncuestaListResponse: Lista paginada de encuestas con metadatos
    """
    # Construir filtros dinámicamente
    filtros = {}
    if id_organizacion is not None:
        filtros['id_organizacion'] = id_organizacion
    if edad_minima is not None:
        filtros['edad_minima'] = edad_minima
    if edad_maxima is not None:
        filtros['edad_maxima'] = edad_maxima
    
    return await encuesta_service.listar_encuestas(
        db, 
        pagina=pagina, 
        tamanio_pagina=tamanio_pagina,
        filtros=filtros
    )


@router.get(
    "/respuestas/{encuesta_id}",
    response_model=EncuestaResponse,
    summary="Obtener respuesta de encuesta por ID",
    description="Recupera una respuesta específica de encuesta usando su ID único"
)
async def obtener_respuesta_encuesta(
    encuesta_id: int,
    db: AsyncSession = Depends(get_db),
    encuesta_service: EncuestaService = Depends(get_encuesta_service)
):
    """
    Obtiene una respuesta específica de encuesta por su ID.
    
    Args:
        encuesta_id: ID único de la encuesta a buscar
        db: Sesión de base de datos
        encuesta_service: Servicio de lógica de negocio
        
    Returns:
        EncuestaResponse: Datos completos de la encuesta
        
    Raises:
        HTTPException 404: Si no se encuentra la encuesta
    """
    encuesta = await encuesta_service.obtener_encuesta_por_id(db, encuesta_id)
    
    if not encuesta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró encuesta con ID {encuesta_id}"
        )
    
    return encuesta


@router.get(
    "/estadisticas/resumen",
    summary="Estadísticas básicas de encuestas",
    description="Obtiene estadísticas generales sobre las respuestas registradas"
)
async def obtener_estadisticas_basicas(
    id_organizacion: Optional[int] = Query(None, description="Filtrar estadísticas por organización"),
    db: AsyncSession = Depends(get_db),
    encuesta_service: EncuestaService = Depends(get_encuesta_service)
):
    """
    Proporciona estadísticas básicas sobre las encuestas registradas.
    
    Útil para dashboards y reportes gerenciales, incluye conteos totales,
    promedios de variables clave y distribuciones demográficas.
    
    Args:
        id_organizacion: Filtro opcional por organización
        db: Sesión de base de datos
        encuesta_service: Servicio de lógica de negocio
        
    Returns:
        dict: Diccionario con estadísticas generales
    """
    return await encuesta_service.obtener_estadisticas_basicas(db, id_organizacion)


@router.delete(
    "/respuestas/{encuesta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar respuesta de encuesta",
    description="Elimina permanentemente una respuesta de encuesta (usar con precaución)"
)
async def eliminar_respuesta_encuesta(
    encuesta_id: int,
    db: AsyncSession = Depends(get_db),
    encuesta_service: EncuestaService = Depends(get_encuesta_service)
):
    """
    Elimina una respuesta de encuesta específica.
    
    ATENCIÓN: Esta operación es irreversible. En producción podrías
    considerar implementar soft deletes en lugar de eliminación física.
    
    Args:
        encuesta_id: ID de la encuesta a eliminar
        db: Sesión de base de datos
        encuesta_service: Servicio de lógica de negocio
        
    Raises:
        HTTPException 404: Si no se encuentra la encuesta
    """
    eliminada = await encuesta_service.eliminar_encuesta(db, encuesta_id)
    
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró encuesta con ID {encuesta_id}"
        )