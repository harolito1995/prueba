# Pregunta 2: Procesador Avanzado de Archivos

## 📋 Descripción

Un procesador de archivos en Python que permite listar archivos, analizar datos de archivos CSV y procesar imágenes médicas DICOM. El proyecto está diseñado para ser modular, fácil de entender y extender, con capacidades avanzadas de análisis y procesamiento de datos.

## 🚀 Características

- **Listado de archivos**: Muestra contenido de carpetas con detalles opcionales (tamaño, fecha de modificación)
- **Análisis de CSV**: Analiza automáticamente todas las columnas, calculando estadísticas para datos numéricos y frecuencias para datos categóricos
- **Procesamiento de DICOM**: Lee archivos de imágenes médicas, extrae metadatos y convierte imágenes a formato PNG
- **Generación de reportes**: Crea reportes automáticos de análisis de datos
- **Manejo de errores**: Sistema robusto de logging y manejo de excepciones
- **Limpieza automática**: Los logs se limpian automáticamente en cada ejecución

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **pydicom**: Procesamiento de archivos DICOM
- **pillow**: Manipulación de imágenes
- **numpy**: Operaciones numéricas
- **pandas**: Análisis de datos CSV
- **logging**: Sistema de registro de eventos

## 📦 Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/technical-test-imexhs.git
   cd technical-test-imexhs/file-processor
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Uso Básico

```bash
python main.py
```

Esto ejecutará:
- Limpieza automática del log
- Listado del contenido de `data/test_folder`
- Análisis del archivo CSV con generación de reporte
- Procesamiento del archivo DICOM con extracción de imagen

## 📁 Estructura del Proyecto

```
file-processor/
├── data/
│   └── test_folder/          # Archivos de prueba
│       ├── sample-02-csv.csv
│       └── sample-02-dicom.dcm
├── file_processor.py         # Clase principal de procesamiento
├── main.py                   # Script de ejecución
├── logs/
│   └── processor.log         # Log de errores (se limpia automáticamente)
├── reports/                  # Reportes generados
├── requirements.txt          # Dependencias
└── README.md
```

## 🔧 API de la Clase FileProcessor

### Inicialización
```python
from file_processor import FileProcessor

processor = FileProcessor(base_path="./data", log_file="./logs/processor.log")
```

### Métodos disponibles

#### `list_folder_contents(folder_name, details=False)`
Lista archivos y carpetas en una ruta específica.
```python
processor.list_folder_contents("test_folder", details=True)
```

#### `read_csv(filename, report_path=None, summary=False)`
Analiza un archivo CSV y genera estadísticas.
```python
processor.read_csv("test_folder/data.csv", report_path="./reports", summary=True)
```

#### `read_dicom(filename, tags=None, extract_image=False)`
Procesa un archivo DICOM y extrae metadatos/imágenes.
```python
processor.read_dicom("test_folder/image.dcm", 
                    tags=[(0x0010, 0x0010), (0x0008, 0x0060)], 
                    extract_image=True)
```

## 🔧 Personalización y Extensión

### Agregar nuevos archivos
1. Coloca tus archivos CSV o DICOM en `data/test_folder/`
2. Modifica `main.py` para procesar tus archivos:
   ```python
   processor.read_csv("test_folder/tu_archivo.csv", report_path="./reports")
   processor.read_dicom("test_folder/tu_imagen.dcm", extract_image=True)
   ```

### Extender funcionalidades
La clase `FileProcessor` está diseñada para ser extensible. Puedes agregar nuevos métodos para:
- Procesar otros tipos de archivos
- Implementar análisis estadísticos adicionales
- Agregar validaciones específicas
- Integrar con bases de datos

### Manejo de errores
Todos los errores se registran en `logs/processor.log` y se muestran mensajes claros en consola. El log se limpia automáticamente en cada ejecución.

## 📊 Dependencias

- `pydicom`: Para procesamiento de archivos DICOM
- `pillow`: Para manipulación de imágenes
- `numpy`: Para operaciones numéricas (incluido con pydicom)

## 📈 Ejemplos de Salida

### Análisis de CSV
```
Columns: ['PatientID', 'Age', 'Weight', 'Height', 'Cholesterol', 'HeartRate']
Rows: 52
Numeric Columns:
  - Age: Average = 31.08, Std Dev = 7.41
  - Weight: Average = 75.96, Std Dev = 4.49
```

### Procesamiento de DICOM
```
Patient Name: Rubo DEMO
Study Date: 19941013
Modality: XA
Extracted image saved to ./data/test_folder/sample-02-dicom.png
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado como parte de un test técnico para demostrar habilidades en procesamiento de archivos, análisis de datos y manejo de formatos médicos.**



