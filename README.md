# Prueba Técnica para Rol de Desarrollador

Este repositorio contiene las soluciones para una evaluación técnica compuesta por 4 desafíos de programación que cubren algoritmos de Python, procesamiento de archivos, desarrollo de API REST y desarrollo frontend con Angular.

## 📁 Estructura del Proyecto

```
technical-test-imexhs/
├── README.md
├── hanoi-recursion/
│   └── README.md
├── file-processor/
│   └── README.md
├── pregunta_3/
│   └── README.md
└── stain-area-calculator/
    └── README.md
```

## 📋 Descripción de las Soluciones

### Pregunta 1: Recursión y Colores
**Torres de Hanoi con Restricciones de Color**

Solución recursiva al clásico problema de las Torres de Hanoi con una restricción adicional: los discos del mismo color no pueden colocarse directamente uno encima del otro.

**Tecnologías**: Python 3.x, Algoritmos recursivos

### Pregunta 2: Manejo de Archivos y Operaciones con Arrays
**Procesador Avanzado de Archivos**

Utilidad completa de procesamiento de archivos que maneja varios formatos incluyendo archivos CSV y DICOM con capacidades de análisis detallado y registro de eventos.

**Tecnologías**: Python 3.x, pydicom, pillow, numpy

### Pregunta 3: API RESTful
**API de Resultados de Procesamiento de Imágenes Médicas**

API REST robusta para gestionar resultados de procesamiento de imágenes médicas con operaciones CRUD completas, validación de datos y normalización.

**Tecnologías**: Python 3.11+, FastAPI, PostgreSQL, SQLAlchemy, Alembic

### Pregunta 4: Aplicación Angular
**Calculadora de Área de Manchas en Imágenes Binarias**

Aplicación Angular que calcula el área de manchas en imágenes binarias utilizando el método Monte Carlo con muestreo de puntos aleatorios.

**Tecnologías**: Angular 20, TypeScript, Angular Material, SCSS

## 🚀 Instrucciones de Ejecución

Cada proyecto tiene su propio archivo README con instrucciones detalladas de instalación y ejecución. Navega a la carpeta correspondiente y sigue las instrucciones específicas:

```bash
# Para cualquier proyecto
cd [nombre-del-proyecto]/
# Leer el README específico del proyecto
```

### Resumen de Comandos por Proyecto

#### Pregunta 1: Torres de Hanoi
```bash
cd hanoi-recursion/
python solucion_hanoi.py
```

#### Pregunta 2: Procesador de Archivos
```bash
cd file-processor/
pip install -r requirements.txt
python main.py
```

#### Pregunta 3: API REST
```bash
cd pregunta_3/
# Opción 1: Docker (recomendado)
docker-compose up -d

# Opción 2: Instalación manual
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Pregunta 4: Aplicación Angular
```bash
cd stain-area-calculator/
npm install
ng serve -o
```

## 📝 Notas Adicionales

- Cada solución incluye su propia documentación detallada
- Los proyectos priorizan la legibilidad y mantenibilidad del código
- Se implementa manejo de errores y registro de eventos
- El código sigue las mejores prácticas de cada tecnología utilizada
- Todos los proyectos incluyen ejemplos de uso y casos de prueba

## 🔧 Requisitos del Sistema

### Para Proyectos Python (Preguntas 1, 2, 3)
- Python 3.11+ (recomendado)
- pip para gestión de dependencias
- PostgreSQL 15+ (solo para Pregunta 3)
- Docker (opcional, para Pregunta 3)

### Para Proyecto Angular (Pregunta 4)
- Node.js >= 18.x
- npm >= 9.x
- Navegador web moderno

## 📊 Características Destacadas

### Algoritmos y Lógica
- **Pregunta 1**: Implementación recursiva con validaciones de color
- **Pregunta 2**: Procesamiento multi-formato con análisis estadístico
- **Pregunta 3**: API REST completa con base de datos relacional
- **Pregunta 4**: Interfaz de usuario moderna con cálculos en tiempo real

---

**Nota**: Cada carpeta de pregunta contiene su propio README detallado con instrucciones específicas de configuración, detalles de implementación y ejemplos de uso. 