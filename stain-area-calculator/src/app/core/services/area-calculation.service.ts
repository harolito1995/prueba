import { Injectable } from '@angular/core';
import { Observable, of, throwError, catchError, tap, map, switchMap } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Calculation } from '../models/calculation.model';
import { ImageProcessingService } from './image-processing.service';
import { StorageService } from './storage.service';
import { Point, ImageSize } from '../interfaces/app.interfaces';

@Injectable({
  providedIn: 'root'
})
export class AreaCalculationService {
  constructor(
    private imageProcessingService: ImageProcessingService,
    private storageService: StorageService,
    private snackBar: MatSnackBar
  ) {}

  // Método principal que implementa el algoritmo Monte Carlo
  // Genera puntos aleatorios y calcula el área de la mancha
  calculateArea(numPoints: number): Observable<Calculation> {
    try {
      if (numPoints <= 0) {
        const error = new Error('El número de puntos debe ser mayor a 0');
        this.showError('El número de puntos debe ser mayor a 0');
        return throwError(() => error);
      }

      const canvas = this.imageProcessingService.getCanvas();
      if (!canvas) {
        const error = new Error('No hay imagen cargada para calcular el área');
        this.showError('Primero debes cargar una imagen');
        return throwError(() => error);
      }

      return this.generateRandomPoints(numPoints, canvas.width, canvas.height).pipe(
        map(points => {
          try {
            const pointsInStain = this.imageProcessingService.countPointsInStain(points);
            const totalArea = canvas.width * canvas.height;
            const stainArea = (pointsInStain / numPoints) * totalArea;

            const calculation: Calculation = {
              id: this.generateId(),
              timestamp: new Date(),
              numPoints,
              pointsInStain,
              totalArea,
              stainArea,
              imageUrl: this.imageProcessingService.getCurrentImageUrl() || ''
            };

            this.showSuccess(`Área calculada: ${stainArea.toFixed(2)} píxeles cuadrados`);

            return calculation;
          } catch (error) {
            this.showError('Error durante el cálculo del área');
            throw error;
          }
        }),
        switchMap(calculation => {
          return this.storageService.saveCalculation(calculation).pipe(
            map(() => calculation)
          );
        }),
        catchError((error: unknown) => {
          this.showError('Error al calcular el área');
          return throwError(() => error);
        })
      );
    } catch (error) {
      this.showError('Error inesperado al calcular el área');
      return throwError(() => error);
    }
  }

  // Genera puntos aleatorios dentro del área de la imagen
  private generateRandomPoints(numPoints: number, width: number, height: number): Observable<Point[]> {
    return new Observable<Point[]>(observer => {
      try {
        const points: Point[] = [];

        for (let i = 0; i < numPoints; i++) {
          try {
            const x = Math.floor(Math.random() * width);
            const y = Math.floor(Math.random() * height);
            points.push({ x, y });
          } catch (error) {
          }
        }

        observer.next(points);
        observer.complete();
      } catch (error) {
        observer.error(error);
      }
    });
  }

  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  private showSuccess(message: string): void {
    try {
      this.snackBar.open(message, 'Cerrar', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'bottom',
        panelClass: ['success-snackbar']
      });
    } catch (error) {
    }
  }

  private showError(message: string): void {
    try {
      this.snackBar.open(message, 'Cerrar', {
        duration: 5000,
        horizontalPosition: 'center',
        verticalPosition: 'bottom',
        panelClass: ['error-snackbar']
      });
    } catch (error) {
    }
  }
}
