// Modelo para los cálculos 

export interface Calculation {
  id: string;
  timestamp: Date;
  numPoints: number;
  pointsInStain: number;
  totalArea: number;
  stainArea: number;
  imageUrl: string;
} 