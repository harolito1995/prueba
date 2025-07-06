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

## 🛠️ Tecnologías Utilizadas.

- **Frontend**: Angular 20, TypeScript
- **UI Framework**: Angular Material
- **Estilos**: SCSS con variables y mixins
- **Algoritmos**: Método Monte Carlo para cálculo de áreas
- **Almacenamiento**: LocalStorage para historial

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
│   │   │   ├── material/
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

### Opción 1: Usando npm start (Recomendado)
```bash
npm start
```

### Opción 2: Usando Angular CLI
```bash
ng serve
```


