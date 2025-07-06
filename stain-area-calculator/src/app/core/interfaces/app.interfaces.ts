// Interfaces para el cálculo de áreas
export interface Point {
  x: number;
  y: number;
}

export interface CalculationResult {
  id: string;
  timestamp: Date;
  fileName: string;
  imageSize: {
    width: number;
    height: number;
  };
  points: Point[];
  area: number;
  perimeter: number;
  confidence: number;
  processingTime: number;
  metadata?: {
    description?: string;
    tags?: string[];
    notes?: string;
  };
}

export interface CalculationSettings {
  numberOfPoints: number;
  precision: number;
  unit: 'mm' | 'cm' | 'm';
  autoSave: boolean;
  showGrid: boolean;
  showPoints: boolean;
  showArea: boolean;
  showPerimeter: boolean;
}

export interface ImageData {
  file: File;
  url: string;
  width: number;
  height: number;
  type: string;
  size: number;
}

export interface ProcessingOptions {
  threshold: number;
  blurRadius: number;
  edgeDetection: boolean;
  noiseReduction: boolean;
}

// Interfaces para el historial
export interface HistoryEntry {
  id: string;
  timestamp: Date;
  fileName: string;
  area: number;
  perimeter: number;
  thumbnail?: string;
}

// Interfaces para la exportación
export interface ExportOptions {
  format: 'json' | 'csv' | 'excel' | 'pdf';
  includeImage: boolean;
  includeMetadata: boolean;
  includeStatistics: boolean;
}

// Interfaces para la configuración de la aplicación
export interface AppSettings {
  theme: 'light' | 'dark' | 'auto';
  language: 'es' | 'en';
  autoBackup: boolean;
  backupInterval: number;
  maxHistoryEntries: number;
  defaultSettings: CalculationSettings;
}

// Interfaces para errores
export interface AppError {
  code: string;
  message: string;
  details?: any;
  timestamp: Date;
}

// Interfaces para eventos
export interface AppEvent {
  type: string;
  data: any;
  timestamp: Date;
}

// Interfaces para estadísticas
export interface Statistics {
  totalCalculations: number;
  averageArea: number;
  averagePerimeter: number;
  totalProcessingTime: number;
  mostUsedSettings: Partial<CalculationSettings>;
  recentCalculations: CalculationResult[];
}

export interface ImageSize {
  width: number;
  height: number;
} 