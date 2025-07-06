import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, finalize, of, EMPTY } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatSliderModule } from '@angular/material/slider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';

import { FileUploadComponent } from '../../shared/components/file-upload/file-upload.component';
import { PointsSliderComponent } from '../../shared/components/points-slider/points-slider.component';
import { ImageProcessingService } from '../../core/services/image-processing.service';
import { AreaCalculationService } from '../../core/services/area-calculation.service';
import { Calculation } from '../../core/models/calculation.model';
import { FormatNumberPipe } from '../../shared/pipes/format-number.pipe';

@Component({
  selector: 'app-calculator',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatCardModule,
    MatSliderModule,
    MatProgressSpinnerModule,
    MatIconModule,
    FileUploadComponent,
    PointsSliderComponent,
    FormatNumberPipe
  ],
  templateUrl: './calculator.component.html',
  styleUrls: ['./calculator.component.scss']
})
export class CalculatorComponent {
  // Inyección de dependencias usando inject() de Angular 20
  private readonly imageProcessingService = inject(ImageProcessingService);
  private readonly areaCalculationService = inject(AreaCalculationService);
  private readonly router = inject(Router);
  private readonly snackBar = inject(MatSnackBar);

  // Signals para estado reactivo
  readonly isImageLoaded = signal<boolean>(false);
  readonly isCalculating = signal<boolean>(false);
  readonly currentCalculation = signal<Calculation | null>(null);
  readonly numPoints = signal<number>(1000);
  readonly imageUrl = signal<string>('');

  // Convertir observables a signals usando toSignal()
  readonly imageLoaded$ = toSignal(this.imageProcessingService.imageLoaded$);

  // Variables para mensajes
  calculationError: string | null = null;
  calculationSuccess: string | null = null;

  constructor() {
    // Effect para reaccionar a cambios en el estado de la imagen
    effect(() => {
      const isLoaded = this.imageLoaded$() ?? false;
      this.isImageLoaded.set(isLoaded);
      
      if (isLoaded) {
        const imageUrl = this.imageProcessingService.getCurrentImageUrl();
        if (imageUrl) {
          this.imageUrl.set(imageUrl);
        }
      } else {
        this.imageUrl.set('');
      }
    });
  }

  onFileSelected(file: File): void {
    // Procesa la imagen seleccionada por el usuario
    try {
      this.isCalculating.set(true);
      
      this.imageProcessingService.loadImage(file)
        .pipe(
          catchError(error => {
            this.showError('Error al cargar la imagen');
            return EMPTY;
          }),
          finalize(() => {
            this.isCalculating.set(false);
          })
        )
        .subscribe({
          next: () => {
            this.showSuccess('Imagen cargada correctamente');
          },
          error: (error) => {
            this.showError('Error al procesar la imagen');
          }
        });
    } catch (error) {
      this.showError('Error al seleccionar el archivo');
      this.isCalculating.set(false);
    }
  }

  onPointsChanged(points: number): void {
    // Actualiza el número de puntos para el cálculo
    try {
      this.numPoints.set(points);
    } catch (error) {
      // Error silencioso
    }
  }

  calculateArea(): void {
    // Ejecuta el cálculo de área usando el método Monte Carlo
    try {
      this.calculationError = null;
      this.calculationSuccess = null;
      
      if (!this.isImageLoaded()) {
        this.calculationError = 'Primero debes cargar una imagen.';
        this.showError('Primero debes cargar una imagen');
        return;
      }

      this.isCalculating.set(true);

      this.areaCalculationService.calculateArea(this.numPoints())
        .pipe(
          catchError(error => {
            this.calculationError = 'Error al calcular el área.';
            this.showError('Error al calcular el área');
            return EMPTY;
          }),
          finalize(() => {
            this.isCalculating.set(false);
          })
        )
        .subscribe({
          next: (calculation) => {
            try {
              this.currentCalculation.set(calculation);
              this.calculationSuccess = `Cálculo completado: ${calculation.stainArea.toFixed(2)} píxeles cuadrados.`;
              this.showSuccess(`Cálculo completado: ${calculation.stainArea.toFixed(2)} píxeles cuadrados`);
            } catch (error) {
              this.calculationError = 'Error al procesar el resultado.';
              this.showError('Error al procesar el resultado');
            }
          },
          error: (error) => {
            this.calculationError = 'Error durante el cálculo.';
            this.showError('Error durante el cálculo');
          }
        });
    } catch (error) {
      this.calculationError = 'Error inesperado al calcular el área.';
      this.showError('Error inesperado al calcular el área');
      this.isCalculating.set(false);
    }
  }

  navigateToHistory(): void {
    // Navega a la página de historial
    try {
      this.router.navigate(['/history']);
    } catch (error) {
      this.showError('Error al navegar al historial');
    }
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
      // Error silencioso al mostrar notificación
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
      // Error silencioso al mostrar notificación
    }
  }
} 