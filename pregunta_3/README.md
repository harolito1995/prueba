# Pregunta 3: API RESTful para Gestión de Resultados de Procesamiento de Imágenes Médicas

## 📋 Descripción

Una API RESTful para gestionar resultados de procesamiento de imágenes médicas usando FastAPI y PostgreSQL. La API proporciona operaciones CRUD completas con validación de datos, normalización automática y capacidades avanzadas de filtrado.

## Requisitos

- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

## Instalación

### Opción 1: Usando Docker (Recomendado)

1. Clona el repositorio
2. Ejecuta con Docker Compose:

```bash
docker-compose up -d
```

Esto iniciará:
- Base de datos PostgreSQL en el puerto 5432
- Aplicación FastAPI en el puerto 8000

### Opción 2: Instalación Manual

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```

2. Configura la base de datos PostgreSQL:

```bash
createdb medical_db
```

3. Configura las variables de entorno en `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/medical_db
DEBUG=True
```

4. Ejecuta la aplicación:

```bash
uvicorn main:app --reload
```

## 🔗 Endpoints de la API

### Crear Resultados de Procesamiento
- **POST** `/api/elements/`
- **Body**: Carga JSON con datos de procesamiento
- **Response**: Lista de resultados de procesamiento creados

Ejemplo de carga:
```json
{
  "1": {
    "id": "aabbcc1",
    "data": [
      "78 83 21 68 96 46 40 11 1 88",
      "58 75 71 69 33 14 15 93 18 54"
    ],
    "deviceName": "CT SCAN"
  }
}
```

### Obtener Todos los Resultados de Procesamiento
- **GET** `/api/elements/`
- **Parámetros de Consulta**:
  - `skip`: Número de registros a omitir (por defecto: 0)
  - `limit`: Número máximo de registros a devolver (por defecto: 100)
  - `created_date_from`: Filtrar por fecha de creación (desde)
  - `created_date_to`: Filtrar por fecha de creación (hasta)
  - `updated_date_from`: Filtrar por fecha de actualización (desde)
  - `updated_date_to`: Filtrar por fecha de actualización (hasta)
  - `avg_before_min`: Promedio mínimo antes de la normalización
  - `avg_before_max`: Promedio máximo antes de la normalización
  - `avg_after_min`: Promedio mínimo después de la normalización
  - `avg_after_max`: Promedio máximo después de la normalización
  - `data_size_min`: Tamaño mínimo de datos
  - `data_size_max`: Tamaño máximo de datos

### Obtener un Resultado de Procesamiento
- **GET** `/api/elements/{id}`
- **Response**: Un resultado de procesamiento

### Actualizar Resultado de Procesamiento
- **PUT** `/api/elements/{id}`
- **Body**: JSON con campos a actualizar
- **Response**: Resultado de procesamiento actualizado

Ejemplo de carga de actualización:
```json
{
  "device_name": "MRI SCANNER",
  "id": "new_id_123"
}
```

### Eliminar Resultado de Procesamiento
- **DELETE** `/api/elements/{id}`
- **Response**: Mensaje de éxito

### Verificación de Estado
- **GET** `/health`
- **Response**: Estado de salud de la API

## 🔄 Procesamiento de Datos

La API procesa automáticamente los datos entrantes:

1. **Validación**: Asegura que todos los elementos de datos sean números válidos
2. **Normalización**: Convierte los datos a escala 0-1 usando el valor máximo
3. **Estadísticas**: Calcula promedios antes y después de la normalización
4. **Almacenamiento**: Guarda los resultados procesados y los datos originales

## 🗄️ Esquema de Base de Datos

### Tabla de Dispositivos
- `id`: Clave primaria
- `device_name`: Nombre único del dispositivo
- `created_date`: Marca de tiempo de creación

### Tabla de Resultados de Procesamiento
- `id`: Clave primaria (desde los datos de entrada)
- `device_id`: Clave foránea a la tabla de dispositivos
- `average_before_normalization`: Promedio antes del procesamiento
- `average_after_normalization`: Promedio después del procesamiento
- `data_size`: Número de puntos de datos
- `raw_data`: Datos de entrada originales (JSON)
- `created_date`: Marca de tiempo de creación
- `updated_date`: Última marca de tiempo de actualización

## 📝 Registro de Logs

La API registra todas las solicitudes, respuestas y errores en:
- Salida de consola
- Archivo `api.log`

## 🧪 Pruebas

Prueba la API usando la documentación interactiva en:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## 📖 Ejemplo de Uso

```bash
# Crear resultados de procesamiento
curl -X POST "http://localhost:8000/api/elements/" \
  -H "Content-Type: application/json" \
  -d '{
    "1": {
      "id": "test123",
      "data": ["10 20 30", "40 50 60"],
      "deviceName": "CT SCAN"
    }
  }'

# Obtener todos los resultados
curl "http://localhost:8000/api/elements/"

# Obtener resultado específico
curl "http://localhost:8000/api/elements/test123"

# Actualizar resultado
curl -X PUT "http://localhost:8000/api/elements/test123" \
  -H "Content-Type: application/json" \
  -d '{"device_name": "MRI SCANNER"}'

# Eliminar resultado
curl -X DELETE "http://localhost:8000/api/elements/test123"
```

## ⚠️ Manejo de Errores

La API devuelve códigos de estado HTTP apropiados:
- `200`: Éxito
- `400`: Solicitud Incorrecta (errores de validación)
- `404`: No Encontrado
- `500`: Error Interno del Servidor

Todos los errores se registran e incluyen mensajes de error descriptivos.