from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from api.database.conexion import Base

class EstadosMexico(Base):
    """
    Modelo SQLAlchemy para la tabla estados_mexico
    Contiene los estados de México para referencias en encuestas
    """
    __tablename__ = "estados_mexico"
    
    id_estado = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_estado = Column(String(100), nullable=False, unique=True)


class MunicipiosMexico(Base):
    """
    Modelo SQLAlchemy para la tabla municipios_mexico
    Contiene los municipios de México para referencias en encuestas
    """
    __tablename__ = "municipios"
    
    id_municipio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_estado = Column(Integer, nullable=False, index=True)
    nombre_municipio = Column(String(100), nullable=False)


class RolesOrganizacion(Base):
    """
    Modelo SQLAlchemy para la tabla roles_organizacion
    Contiene los roles dentro de una organización para referencias en encuestas
    """
    __tablename__ = "roles_organizacion"
    
    id_rol_organizacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_rol = Column(String(100), nullable=False, unique=True)


class EncuestaLaboralSaludMental(Base):
    """
    Modelo SQLAlchemy para la tabla encuesta_laboral_salud_mental
    Representa una respuesta completa de la encuesta de salud mental laboral
    """
    __tablename__ = "encuesta_laboral_salud_mental"
    
    # Campo ID automático (primary key)
    id_respuesta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Datos básicos del encuestado
    id_organizacion = Column(Integer, nullable=False, index=True)
    apellidos = Column(String(100), nullable=False)
    nombres = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    id_genero = Column(Integer, nullable=False)
    id_rol_organizacion = Column(Integer, nullable=False)
    anos_organizacion = Column(Integer, nullable=False)
    horas_semanales = Column(Integer, nullable=False)
    id_porcentaje_trabajo_remoto = Column(Integer, nullable=False)
    
    # Variables de salud mental (Escala likert intensidad)
    id_nivel_placer_interes = Column(Integer, nullable=False)
    id_nivel_tristeza_desesperanza = Column(Integer, nullable=False)
    id_nivel_problemas_sueno = Column(Integer, nullable=False)
    id_nivel_disminucion_energia = Column(Integer, nullable=False)
    id_nivel_cambio_apetito = Column(Integer, nullable=False)
    id_nivel_decepcion_personal = Column(Integer, nullable=False)
    id_nivel_problemas_concentracion = Column(Integer, nullable=False)
    id_nivel_movimientos_involuntarios = Column(Integer, nullable=False)
    id_nivel_tentacion_no_levantarse = Column(Integer, nullable=False)
    
    # Variables de ambiente laboral (Escala likert frecuencia)
    id_frecuencia_limitacion_convivencia = Column(Integer, nullable=False)
    id_frecuencia_desacreditar_profesionalismo = Column(Integer, nullable=False)
    id_frecuencia_desprestigio = Column(Integer, nullable=False)
    id_frecuencia_informar_mal_permanencia = Column(Integer, nullable=False)
    
    # Variables sociodemográficas
    id_nivel_estudios = Column(Integer, nullable=False)
    id_estado_nacimiento = Column(Integer, nullable=False)
    id_estado_mas_anos = Column(Integer, nullable=False)
    id_estado_civil_padres = Column(Integer, nullable=False)
    
    # Antecedentes familiares de salud (Escala si/no)
    id_familiares_diabetes = Column(Integer, nullable=False)
    id_familiares_cancer = Column(Integer, nullable=False)
    id_familiares_cerebrovascular = Column(Integer, nullable=False)
    
    # Metadatos automáticos
    #fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    #fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())