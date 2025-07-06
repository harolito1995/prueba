export const APP_CONSTANTS = {
  // Configuración de la aplicación
  APP_NAME: 'Stain Area Calculator',
  APP_VERSION: '1.0.0',
  
  // Configuración de archivos
  SUPPORTED_IMAGE_TYPES: ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'],
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  
  // Configuración de cálculos
  DEFAULT_POINTS: 100,
  MIN_POINTS: 10,
  MAX_POINTS: 1000,
  
  // Configuración de almacenamiento
  STORAGE_KEY: 'stain_calculator_data',
  HISTORY_KEY: 'calculation_history',
  
  // Configuración de UI
  SNACKBAR_DURATION: 3000,
  DEBOUNCE_TIME: 300,
  
  // Configuración de API (si se implementa en el futuro)
  API_BASE_URL: 'http://localhost:3000/api',
  API_TIMEOUT: 30000,
  
  // Configuración de gráficos
  CHART_COLORS: {
    primary: '#3f51b5',
    secondary: '#ff4081',
    success: '#4caf50',
    warning: '#ff9800',
    error: '#f44336',
    info: '#2196f3'
  },
  
  // Configuración de precisión
  DECIMAL_PLACES: 4,
  AREA_UNIT: 'mm²',
  PERIMETER_UNIT: 'mm'
};

export const ERROR_MESSAGES = {
  FILE_TOO_LARGE: 'El archivo es demasiado grande. Máximo 10MB.',
  UNSUPPORTED_FILE_TYPE: 'Tipo de archivo no soportado. Use JPG, PNG, BMP o TIFF.',
  FILE_READ_ERROR: 'Error al leer el archivo.',
  CALCULATION_ERROR: 'Error durante el cálculo.',
  NO_IMAGE_SELECTED: 'Por favor seleccione una imagen.',
  INSUFFICIENT_POINTS: 'Se necesitan al menos 10 puntos para el cálculo.',
  NETWORK_ERROR: 'Error de conexión. Verifique su internet.',
  UNKNOWN_ERROR: 'Ha ocurrido un error inesperado.'
};

export const SUCCESS_MESSAGES = {
  FILE_UPLOADED: 'Archivo cargado exitosamente.',
  CALCULATION_COMPLETED: 'Cálculo completado exitosamente.',
  DATA_SAVED: 'Datos guardados exitosamente.',
  DATA_EXPORTED: 'Datos exportados exitosamente.',
  SETTINGS_UPDATED: 'Configuración actualizada.'
}; 