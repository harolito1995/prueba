# Pregunta 4: Calculadora de Área de Manchas en Imágenes Binarias

## 📋 Descripción

**Stain Area Calculator** es una aplicación web desarrollada en Angular 20 que permite calcular áreas de manchas o regiones irregulares en imágenes utilizando el método de Monte Carlo. Es ideal para aplicaciones científicas, educativas o de ingeniería donde se requiere estimar áreas de forma visual e interactiva.

## 🚀 Características

- **Carga de imágenes**: Soporte para múltiples formatos de imagen
- **Método Monte Carlo**: Cálculo de áreas mediante muestreo de puntos aleatorios
- **Control de precisión**: Ajuste dinámico del número de puntos de muestreo
- **Visualización en tiempo real**: Resultados instantáneos con métricas de precisión
- **Historial de cálculos**: Almacenamiento local de resultados anteriores
- **Interfaz moderna**: Diseño responsive con Angular Material
- **Arquitectura modular**: Código organizado en features y componentes reutilizables
- **Angular 20**: Control Flow Blocks (@if, @for) y Signals modernos


## 📁 Estructura del Proyecto

```
stain-area-calculator/
├── angular.json
├── package.json
├── README.md
├── src/
│   ├── app/
│   │   ├── app.component.*
│   │   ├── core/
│   │   │   ├── constants/
│   │   │   ├── interfaces/
│   │   │   ├── models/
│   │   │   └── services/
│   │   ├── features/
│   │   │   ├── calculator/
│   │   │   └── history/
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── file-upload/
│   │   │   │   └── points-slider/
│   │   │   └── pipes/
│   │   └── styles/
│   ├── assets/
│   └── styles.scss
├── public/
└── ...otros archivos de configuración
```

## Requisitos

- Node.js >= 18.x
- npm >= 9.x
- Navegador web moderno

## 📦 Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/technical-test-imexhs.git
   cd technical-test-imexhs/stain-area-calculator
   ```

2. **Instala las dependencias:**
   ```bash
   npm install
   ```

## 🚀 Ejecución

### Opción 1: Usando ng serve -o (Recomendado)
```bash
ng serve -o
```

### Opción 2: Usando npx (si no tienes Angular CLI global)
```bash
npx ng serve -o
```

### Opción 3: Usando npm start
```bash
npm start
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:4200`.

## 🎯 Uso

1. **Cargar imagen**: Haz clic en "Seleccionar imagen" y elige una imagen binaria
2. **Ajustar precisión**: Usa el slider para establecer el número de puntos de muestreo
3. **Calcular área**: Haz clic en "Calcular área" para ejecutar el método Monte Carlo
4. **Ver resultados**: Los resultados se mostrarán con el área calculada y estadísticas
5. **Revisar historial**: Ve a la pestaña "Historial" para ver cálculos anteriores

## 🔧 Desarrollo

### Estructura de Componentes
- **Calculator**: Componente principal para el cálculo de áreas
- **FileUpload**: Componente reutilizable para carga de archivos
- **PointsSlider**: Componente para ajustar la precisión del cálculo
- **History**: Componente para mostrar el historial de cálculos

### Servicios Principales
- **AreaCalculationService**: Implementa el algoritmo Monte Carlo
- **ImageProcessingService**: Maneja el procesamiento de imágenes
- **StorageService**: Gestiona el almacenamiento local de datos

## 📊 Método Monte Carlo

El cálculo de áreas utiliza el método Monte Carlo:
1. Se generan puntos aleatorios sobre la imagen
2. Se cuenta cuántos puntos caen dentro de la mancha
3. Se calcula el área como: `(puntos_en_mancha / total_puntos) * área_total`


