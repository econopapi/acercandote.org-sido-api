# acercándote.org - Sistema Integral para Diagnóstico Organizacional [API+Backend]

Una API REST desarrollada con FastAPI para la recolección y análisis en el Sistema Integral para Diangóstico Organizacional (SIDO). El sistema permite registrar respuestas de encuestas multidimensionales y, en futuras versiones, aplicar algoritmos de clustering para identificar patrones en los datos.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso de la API](#-uso-de-la-api)
- [Documentación de Endpoints](#-documentación-de-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## 🚀 Características

**Funcionalidades Actuales:**
- Registro de respuestas de encuestas de salud mental laboral con validación automática
- Sistema de paginación y filtros para consulta de datos
- Estadísticas básicas y métricas de salud mental por organización
- Documentación interactiva automática con Swagger/OpenAPI
- Arquitectura asíncrona para alto rendimiento
- Validación de datos con Pydantic

**Funcionalidades Planificadas:**
- Algoritmo de clustering K-means multidimensional para análisis de patrones
- Dashboard de visualización de datos
- Reportes automatizados en PDF
- Sistema de alertas por niveles críticos de riesgo

## 🏗️ Arquitectura del Proyecto


```
├── api/
│   ├── routers/          # Controladores REST
│   ├── servicios/         # Lógica de negocio
│   ├── modelos/           # Modelos SQLAlchemy
│   ├── schemas/          # Schemas Pydantic (validación)
│   └── database/         # Configuración de base de datos
```

**Stack Tecnológico:**
- **Backend:** FastAPI (Python 3.9+)
- **Base de Datos:** PostgreSQL
- **ORM:** SQLAlchemy 2.0 con soporte async
- **Validación:** Pydantic v2
- **Servidor ASGI:** Uvicorn

## 📋 Requisitos Previos

Antes de instalar el proyecto, asegurate de tener:

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Una una instancia de PostgreSQL o una cuenta en Supabase
- Git (para clonar el repositorio)

## 🔧 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/econopapi/acercandote.org-sido-api.git
cd acercandote.org-sido-api
```

### 2. Crear y Activar Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/MacOS:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# URL de conexión a PostgreSQL/Supabase
DATABASE_URL=postgresql+asyncpg://postgres:tu_password@tu_host:5432/tu_database

# Configuraciones opcionales
DEBUG=True
API_VERSION=1.0.0
```

### 2. Configuración de Supabase

1. Crea un proyecto en [Supabase](https://supabase.com/)
2. Ve a **Settings > Database** en tu dashboard
3. Copia la **Connection String** y reemplaza los valores en tu archivo `.env`
4. Asegúrate de que la URL incluya `+asyncpg` después de `postgresql`

### 3. Inicializar Base de Datos

La aplicación creará automáticamente las tablas necesarias al iniciar. No necesitas ejecutar migraciones manualmente.

## 🚀 Uso de la API

### Ejecutar el Servidor

```bash
# Opción 1: Usando el script run.py
python start.py

# Opción 2: Usando uvicorn directamente
uvicorn api.main:api --reload --host 127.0.0.1 --port 8000
```

La API estará disponible en:
- **Aplicación:** http://127.0.0.1:8000
- **Documentación Interactiva:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### Verificar Instalación

```bash
curl http://127.0.0.1:8000/estado
# Respuesta esperada: {"status":"healthy"}
```

## 📚 Documentación de Endpoints

### Encuestas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/encuestas/laboral-salud-mental/respuestas` | Registrar nueva respuesta de encuesta |
| GET | `api/v1/encuestas/laboral-salud-mental/respuestas/{encuesta_id}` | Obtener respuesta específica |
| GET | `api/v1/encuestas/laboral-salud-mental/respuestas` | Listar respuestas (paginado) |
| GET | `/api/v1/encuestas/laboral-salud-mental/estadisticas/resumen` | Estadísticas básicas |
| DELETE | `/api/v1/encuestas/laboral-salud-mental/respuestas/{encuesta_id}` | Eliminar respuesta |

### Parámetros de Consulta Disponibles

**Paginación:**
- `pagina`: Número de página (default: 1)
- `tamanio_pagina`: Registros por página (default: 10, máx: 100)

**Filtros:**
- `id_organizacion`: Filtrar por organización específica
- `edad_minima`: Edad mínima del encuestado
- `edad_maxima`: Edad máxima del encuestado

## 📁 Estructura del Proyecto

```
acercandote.org-api-encuestas/
├── api/                          # Código fuente principal
│   ├── __init__.py
│   ├── main.py                   # Aplicación FastAPI principal
│   ├── database/                 # Configuración de base de datos
│   │   ├── __init__.py
│   │   └── conexion.py         # SQLAlchemy engine y sesiones
│   ├── modelos/                   # Modelos de datos (ORM)
│   │   ├── __init__.py
│   │   └── encuesta_laboral_salud_mental.py          # Modelo de encuesta
│   ├── schemas/                  # Schemas de validación (Pydantic)
│   │   ├── __init__.py
│   │   └── encuesta_laboral_salud_mental.py          # Schemas de request/response
│   ├── routers/                  # Controladores REST
│   │   ├── __init__.py
│   │   └── encuesta_laboral_salud_mental.py         # Endpoints de encuestas
│   └── servicios/                 # Lógica
│       ├── __init__.py
│       └── encuesta_laboral_salud_mental.py  # Servicio de encuestas
├── tests/                        # Tests unitarios y de integración
├── requirements.txt              # Dependencias Python
├── start.py                       # Script para ejecutar la aplicación
├── .env                         # Variables de entorno
├── .gitignore                   # Archivos a ignorar por Git
└── README.md                   
```

## 💡 Ejemplos de Uso

### Registrar Nueva Encuesta

```python
import requests
import json

# Datos de ejemplo
encuesta_data = {
    "id_organizacion": 3,
    "apellidos": "García",
    "nombres": "María",
    "edad": 28,
    "id_genero": 1,
    "id_rol_organizacion": 45,
    "anos_organizacion": 2,
    "horas_semanales": 40,
    "id_porcentaje_trabajo_remoto": 2,
    "id_nivel_placer_interes": 3,
    "id_nivel_tristeza_desesperanza": 1,
    "id_nivel_problemas_sueno": 2,
    # ... resto de los campos
}

# Enviar request
response = requests.post(
    "http://127.0.0.1:8000/api/v1/encuestas/laboral-salud-mental/respuestas",
    json=encuesta_data,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 201:
    resultado = response.json()
    print(f"Encuesta creada con ID: {resultado['id']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### Obtener Estadísticas

```javascript
// JavaScript/Node.js example
const obtenerEstadisticas = async (organizacionId = null) => {
    const url = organizacionId 
        ? `http://127.0.0.1:8000/api/v1/encuestas/laboral-salud-mental/estadisticas/resumen?id_organizacion=${organizacionId}`
        : 'http://127.0.0.1:8000/api/v1/encuestas/laboral-salud-mental/estadisticas/resumen';
    
    try {
        const response = await fetch(url);
        const stats = await response.json();
        console.log('Estadísticas:', stats);
        return stats;
    } catch (error) {
        console.error('Error al obtener estadísticas:', error);
    }
};

// Uso
obtenerEstadisticas(3); // Estadísticas para organización ID 3
```

### Listar Encuestas con Filtros

```bash
# Usando curl - obtener encuestas de la organización 3, página 2
curl -X GET "http://127.0.0.1:8000/api/v1/encuestas/respuestas?id_organizacion=3&pagina=2&tamanio_pagina=20" \
     -H "accept: application/json"
```

## 🧪 Testing

Para ejecutar las pruebas (cuando estén implementadas):

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest tests/ -v

# Ejecutar tests con cobertura
pytest tests/ --cov=app --cov-report=html
```

## 🗺️ Roadmap

### Versión 1.1 (Próxima)
- [ ] Implementación de algoritmo K-means para clustering
- [ ] Endpoints para análisis de patrones
- [ ] Mejoras en el sistema de filtros

### Versión 1.2
- [ ] Dashboard web interactivo
- [ ] Exportación de datos a Excel/CSV
- [ ] Sistema de notificaciones por email
- [ ] API de reportes automatizados



### Estándares de Código

- Seguir PEP 8 para estilo de código Python
- Agregar docstrings a todas las funciones públicas
- Incluir tests para nuevas funcionalidades
- Actualizar el README si es necesario

### Reportar Bugs

Usa el sistema de Issues de GitHub e incluí:
- Descripción detallada del problema
- Pasos para reproducir el bug
- Versión de Python y dependencias
- Logs relevantes

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Daniel Limón**
- GitHub: [@econopapi](https://github.com/econopapi)
- Email: dani@dlimon.net

---

⭐ Si este proyecto te resulta útil, ¡dale una estrella en GitHub!