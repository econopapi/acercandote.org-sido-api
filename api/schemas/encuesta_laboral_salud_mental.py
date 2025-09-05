from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class EncuestaCreate(BaseModel):
    """
    Schema para crear una nueva respuesta de encuesta
    Valida todos los datos de entrada del request JSON
    """
    # Datos básicos del encuestado
    id_organizacion: int = Field(..., gt=0, description="ID de la organización")
    apellidos: str = Field(..., min_length=1, max_length=100, description="Apellidos del encuestado")
    nombres: str = Field(..., min_length=1, max_length=100, description="Nombres del encuestado")
    edad: int = Field(..., ge=14, le=100, description="Edad del encuestado")
    id_genero: int = Field(..., ge=0, description="ID del género")
    id_rol_organizacion: int = Field(..., gt=0, description="ID del rol en la organización")
    anos_organizacion: int = Field(..., ge=0, le=60, description="Años en la organización")
    horas_semanales: int = Field(..., ge=1, le=90, description="Horas semanales de trabajo")
    id_porcentaje_trabajo_remoto: int = Field(..., ge=0, description="ID porcentaje trabajo remoto")
    
    # Variables de salud mental (Escala likert intensidad)
    id_nivel_placer_interes: int = Field(..., ge=0, le=5, description="Nivel de placer/interés")
    id_nivel_tristeza_desesperanza: int = Field(..., ge=0, le=5, description="Nivel de tristeza/desesperanza")
    id_nivel_problemas_sueno: int = Field(..., ge=0, le=5, description="Nivel de problemas de sueño")
    id_nivel_disminucion_energia: int = Field(..., ge=0, le=5, description="Nivel de disminución de energía")
    id_nivel_cambio_apetito: int = Field(..., ge=0, le=5, description="Nivel de cambio de apetito")
    id_nivel_decepcion_personal: int = Field(..., ge=0, le=5, description="Nivel de decepción personal")
    id_nivel_problemas_concentracion: int = Field(..., ge=0, le=5, description="Nivel de problemas de concentración")
    id_nivel_movimientos_involuntarios: int = Field(..., ge=0, le=5, description="Nivel de movimientos involuntarios")
    id_nivel_tentacion_no_levantarse: int = Field(..., ge=0, le=5, description="Nivel de tentación de no levantarse")
    
    # Variables de ambiente laboral (Escala likert frecuencia)
    id_frecuencia_limitacion_convivencia: int = Field(..., ge=0, le=5, description="Frecuencia limitación convivencia")
    id_frecuencia_desacreditar_profesionalismo: int = Field(..., ge=0, le=5, description="Frecuencia desacreditar profesionalismo")
    id_frecuencia_desprestigio: int = Field(..., ge=0, le=5, description="Frecuencia de desprestigio")
    id_frecuencia_informar_mal_permanencia: int = Field(..., ge=0, le=5, description="Frecuencia informar mal permanencia")
    
    # Variables sociodemográficas
    id_nivel_estudios: int = Field(..., ge=0, description="ID nivel de estudios")
    id_estado_nacimiento: int = Field(..., ge=0, description="ID estado de nacimiento")
    id_estado_mas_anos: int = Field(..., ge=0, description="ID estado donde más años vivió")
    id_estado_civil_padres: int = Field(..., ge=0, description="ID estado civil de los padres")
    
    # Antecedentes familiares (Escala si/no)
    id_familiares_diabetes: int = Field(..., ge=0, le=4, description="Familiares con diabetes")
    id_familiares_cancer: int = Field(..., ge=0, le=4, description="Familiares con cáncer")
    id_familiares_cerebrovascular: int = Field(..., ge=0, le=4, description="Familiares con problemas cerebrovasculares")

    @validator('apellidos', 'nombres')
    def validate_nombres(cls, v):
        """Validar que nombres y apellidos no estén vacíos después de limpiar espacios"""
        if not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip().title()  # Convertir a formato título

    class Config:
        """Configuración del schema"""
        # Ejemplo de datos válidos para la documentación automática
        schema_extra = {
            "example": {
                "id_organizacion": 3,
                "apellidos": "Limón",
                "nombres": "Daniel",
                "edad": 30,
                "id_genero": 2,
                "id_rol_organizacion": 57,
                "anos_organizacion": 3,
                "horas_semanales": 40,
                "id_porcentaje_trabajo_remoto": 0,
                "id_nivel_placer_interes": 2,
                "id_nivel_tristeza_desesperanza": 2,
                "id_nivel_problemas_sueno": 1,
                "id_nivel_disminucion_energia": 2,
                "id_nivel_cambio_apetito": 3,
                "id_nivel_decepcion_personal": 2,
                "id_nivel_problemas_concentracion": 1,
                "id_nivel_movimientos_involuntarios": 4,
                "id_nivel_tentacion_no_levantarse": 3,
                "id_frecuencia_limitacion_convivencia": 1,
                "id_frecuencia_desacreditar_profesionalismo": 2,
                "id_frecuencia_desprestigio": 3,
                "id_frecuencia_informar_mal_permanencia": 1,
                "id_nivel_estudios": 1,
                "id_estado_nacimiento": 20,
                "id_estado_mas_anos": 6,
                "id_estado_civil_padres": 3,
                "id_familiares_diabetes": 0,
                "id_familiares_cancer": 1,
                "id_familiares_cerebrovascular": 1
            }
        }


class EncuestaResponse(BaseModel):
    """
    Schema para la respuesta al cliente después de crear/obtener una encuesta
    Incluye todos los campos del modelo más metadatos automáticos
    """
    id_organizacion: int
    apellidos: str
    nombres: str
    edad: int
    id_genero: int
    id_rol_organizacion: int
    anos_organizacion: int
    horas_semanales: int
    id_porcentaje_trabajo_remoto: int
    
    # Variables de salud mental
    id_nivel_placer_interes: int
    id_nivel_tristeza_desesperanza: int
    id_nivel_problemas_sueno: int
    id_nivel_disminucion_energia: int
    id_nivel_cambio_apetito: int
    id_nivel_decepcion_personal: int
    id_nivel_problemas_concentracion: int
    id_nivel_movimientos_involuntarios: int
    id_nivel_tentacion_no_levantarse: int
    
    # Variables de ambiente laboral
    id_frecuencia_limitacion_convivencia: int
    id_frecuencia_desacreditar_profesionalismo: int
    id_frecuencia_desprestigio: int
    id_frecuencia_informar_mal_permanencia: int
    
    # Variables sociodemográficas
    id_nivel_estudios: int
    id_estado_nacimiento: int
    id_estado_mas_anos: int
    id_estado_civil_padres: int
    
    # Antecedentes familiares
    id_familiares_diabetes: int
    id_familiares_cancer: int
    id_familiares_cerebrovascular: int
    
    # Metadatos automáticos
    #fecha_creacion: datetime
    #fecha_actualizacion: Optional[datetime] = None

    class Config:
        """Permitir que Pydantic trabaje con objetos SQLAlchemy"""
        from_attributes = True


class EncuestaListResponse(BaseModel):
    """
    Schema para respuesta de listado paginado de encuestas
    Incluye metadatos de paginación
    """
    encuestas: list[EncuestaResponse]
    total: int
    pagina: int
    tamanio_pagina: int
    total_paginas: int