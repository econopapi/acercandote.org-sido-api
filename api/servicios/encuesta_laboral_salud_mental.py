from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from typing import Optional, Dict, Any
from api.modelos.encuesta_laboral_salud_mental import EncuestaLaboralSaludMental
from api.schemas.encuesta_laboral_salud_mental import EncuestaCreate, EncuestaResponse, EncuestaListResponse
import math

class EncuestaService:
    """
    Servicio que maneja toda la lógica de negocio relacionada con las encuestas.
    
    Esta clase separa la lógica de negocio de los controladores (routers),
    facilitando el testing y el mantenimiento del código.
    """
    
    async def crear_encuesta(
        self, 
        db: AsyncSession, 
        encuesta_data: EncuestaCreate
    ) -> EncuestaResponse:
        """
        Crea una nueva respuesta de encuesta en la base de datos.
        
        Args:
            db: Sesión de base de datos
            encuesta_data: Datos validados de la encuesta
            
        Returns:
            EncuestaResponse: Encuesta creada con ID y metadatos
            
        Raises:
            ValueError: Si hay errores de validación de lógica o datos
        """
        # Validaciones adicionales de lógica
        await self._validar_datos_encuesta(db, encuesta_data)
        
        # Crear instancia del modelo SQLAlchemy
        nueva_encuesta = EncuestaLaboralSaludMental(
            **encuesta_data.model_dump()
        )
        
        # Guardar en base de datos
        db.add(nueva_encuesta)
        await db.commit()
        await db.refresh(nueva_encuesta)
        
        # Convertir a schema de respuesta
        return EncuestaResponse.model_validate(nueva_encuesta)
    

    async def obtener_encuesta_por_id(
        self, 
        db: AsyncSession, 
        encuesta_id: int
    ) -> Optional[EncuestaResponse]:
        """
        Obtiene una encuesta específica por su ID.
        
        Args:
            db: Sesión de base de datos
            encuesta_id: ID de la encuesta a buscar
            
        Returns:
            EncuestaResponse o None si no se encuentra
        """
        query = select(EncuestaLaboralSaludMental).where(
            EncuestaLaboralSaludMental.id == encuesta_id
        )
        
        result = await db.execute(query)
        encuesta = result.scalar_one_or_none()
        
        if encuesta:
            return EncuestaResponse.model_validate(encuesta)
        return None
    

    async def listar_encuestas(
        self,
        db: AsyncSession,
        pagina: int = 1,
        tamanio_pagina: int = 25,
        filtros: Optional[Dict[str, Any]] = None
    ) -> EncuestaListResponse:
        """
        Lista encuestas con paginación y filtros opcionales.
        
        Args:
            db: Sesión de base de datos
            pagina: Número de página (comenzando desde 1)
            tamanio_pagina: Cantidad de registros por página
            filtros: Diccionario con filtros opcionales
            
        Returns:
            EncuestaListResponse: Lista paginada con metadatos
        """
        # Construir query base
        query = select(EncuestaLaboralSaludMental)
        count_query = select(func.count(EncuestaLaboralSaludMental.id))
        
        # Aplicar filtros si existen
        if filtros:
            conditions = self._construir_condiciones_filtro(filtros)
            if conditions:
                query = query.where(and_(*conditions))
                count_query = count_query.where(and_(*conditions))
        
        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(desc(EncuestaLaboralSaludMental.fecha_creacion))
        
        # Aplicar paginación
        offset = (pagina - 1) * tamanio_pagina
        query = query.offset(offset).limit(tamanio_pagina)
        
        # Ejecutar consultas
        result = await db.execute(query)
        encuestas = result.scalars().all()
        
        count_result = await db.execute(count_query)
        total = count_result.scalar()
        
        # Convertir a schemas de respuesta
        encuestas_response = [
            EncuestaResponse.model_validate(encuesta) 
            for encuesta in encuestas
        ]
        
        # Calcular metadatos de paginación
        total_paginas = math.ceil(total / tamanio_pagina)
        
        return EncuestaListResponse(
            encuestas=encuestas_response,
            total=total,
            pagina=pagina,
            tamanio_pagina=tamanio_pagina,
            total_paginas=total_paginas
        )
    

    async def obtener_estadisticas_basicas(
        self,
        db: AsyncSession,
        id_organizacion: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene estadísticas básicas de las encuestas.
        
        Args:
            db: Sesión de base de datos
            id_organizacion: Filtro opcional por organización
            
        Returns:
            dict: Estadísticas generales
        """
        # Query base para contar
        query = select(EncuestaLaboralSaludMental)
        
        if id_organizacion:
            query = query.where(EncuestaLaboralSaludMental.id_organizacion == id_organizacion)
        
        # Total de respuestas
        count_query = select(func.count(EncuestaLaboralSaludMental.id))
        if id_organizacion:
            count_query = count_query.where(EncuestaLaboralSaludMental.id_organizacion == id_organizacion)
        
        count_result = await db.execute(count_query)
        total_respuestas = count_result.scalar()
        
        # Promedios de variables clave de salud mental
        avg_queries = {
            'promedio_placer_interes': func.avg(EncuestaLaboralSaludMental.id_nivel_placer_interes),
            'promedio_tristeza': func.avg(EncuestaLaboralSaludMental.id_nivel_tristeza_desesperanza),
            'promedio_problemas_sueno': func.avg(EncuestaLaboralSaludMental.id_nivel_problemas_sueno),
            'promedio_energia': func.avg(EncuestaLaboralSaludMental.id_nivel_disminucion_energia),
            'promedio_concentracion': func.avg(EncuestaLaboralSaludMental.id_nivel_problemas_concentracion)
        }
        
        estadisticas = {
            'total_respuestas': total_respuestas,
            'id_organizacion': id_organizacion
        }
        
        # Solo calcular promedios si hay datos
        if total_respuestas > 0:
            for nombre, query_func in avg_queries.items():
                avg_query = select(query_func)
                if id_organizacion:
                    avg_query = avg_query.where(EncuestaLaboralSaludMental.id_organizacion == id_organizacion)
                
                result = await db.execute(avg_query)
                promedio = result.scalar()
                estadisticas[nombre] = round(promedio, 2) if promedio else 0.0
            
            # Distribución por género
            genero_query = select(
                EncuestaLaboralSaludMental.id_genero,
                func.count(EncuestaLaboralSaludMental.id).label('cantidad')
            ).group_by(EncuestaLaboralSaludMental.id_genero)
            
            if id_organizacion:
                genero_query = genero_query.where(EncuestaLaboralSaludMental.id_organizacion == id_organizacion)
            
            genero_result = await db.execute(genero_query)
            distribucion_genero = {
                f'genero_{row.id_genero}': row.cantidad 
                for row in genero_result
            }
            
            estadisticas['distribucion_genero'] = distribucion_genero
            
            # Promedio de edad
            edad_query = select(func.avg(EncuestaLaboralSaludMental.edad))
            if id_organizacion:
                edad_query = edad_query.where(EncuestaLaboralSaludMental.id_organizacion == id_organizacion)
            
            edad_result = await db.execute(edad_query)
            promedio_edad = edad_result.scalar()
            estadisticas['promedio_edad'] = round(promedio_edad, 1) if promedio_edad else 0.0
        
        return estadisticas
    

    async def eliminar_encuesta(
        self,
        db: AsyncSession,
        encuesta_id: int
    ) -> bool:
        """
        Elimina una encuesta específica.
        
        Args:
            db: Sesión de base de datos
            encuesta_id: ID de la encuesta a eliminar
            
        Returns:
            bool: True si se eliminó, False si no se encontró
        """
        query = select(EncuestaLaboralSaludMental).where(
            EncuestaLaboralSaludMental.id == encuesta_id
        )
        
        result = await db.execute(query)
        encuesta = result.scalar_one_or_none()
        
        if encuesta:
            await db.delete(encuesta)
            await db.commit()
            return True
        
        return False
    

    async def _validar_datos_encuesta(
        self,
        db: AsyncSession,
        encuesta_data: EncuestaCreate
    ) -> None:
        """
        Validaciones adicionales de lógica antes de crear la encuesta.
        
        Args:
            db: Sesión de base de datos
            encuesta_data: Datos de la encuesta a validar
            
        Raises:
            ValueError: Si hay errores de validación
        """
        # Ejemplo: validar que la organización exista (si tenés tabla de organizaciones)
        # if not await self._organizacion_existe(db, encuesta_data.id_organizacion):
        #     raise ValueError(f"La organización {encuesta_data.id_organizacion} no existe")
        
        # Validación de coherencia: años en la organización vs edad
        if encuesta_data.anos_organizacion > (encuesta_data.edad - 18):
            raise ValueError(
                "Los años en la organización no pueden ser mayores que la edad laboral del encuestado"
            )
        
        # Validación de horas semanales razonables
        if encuesta_data.horas_semanales > 90:
            # Solo advertencia, no error crítico, pero podrías logearlo
            pass


    def _construir_condiciones_filtro(self, filtros: Dict[str, Any]) -> list:
        """
        Construye condiciones SQLAlchemy a partir de un diccionario de filtros.
        
        Args:
            filtros: Diccionario con filtros a aplicar
            
        Returns:
            list: Lista de condiciones SQLAlchemy
        """
        conditions = []
        
        if 'id_organizacion' in filtros:
            conditions.append(
                EncuestaLaboralSaludMental.id_organizacion == filtros['id_organizacion']
            )
        
        if 'edad_minima' in filtros:
            conditions.append(
                EncuestaLaboralSaludMental.edad >= filtros['edad_minima']
            )
        
        if 'edad_maxima' in filtros:
            conditions.append(
                EncuestaLaboralSaludMental.edad <= filtros['edad_maxima']
            )
        
        return conditions