import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, finalize, EMPTY } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

import { StorageService } from '../../core/services/storage.service';
import { Calculation } from '../../core/models/calculation.model';
import { FormatNumberPipe } from '../../shared/pipes/format-number.pipe';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    FormatNumberPipe
  ],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent {
  // Inyección de dependencias usando inject() de Angular 20
  private readonly storageService = inject(StorageService);
  private readonly router = inject(Router);
  private readonly snackBar = inject(MatSnackBar);
  private readonly dialog = inject(MatDialog);

  // Signals para estado reactivo
  readonly calculations = signal<Calculation[]>([]);
  readonly isLoading = signal<boolean>(false);
  readonly displayedColumns = ['timestamp', 'numPoints', 'pointsInStain', 'stainArea', 'actions'];

  // Convertir observables a signals usando toSignal()
  readonly calculations$ = toSignal(this.storageService.calculations$);

  // Variables para mensajes
  historyError: string | null = null;
  historySuccess: string | null = null;

  constructor() {
    // Effect para reaccionar a cambios en los cálculos
    effect(() => {
      const calculations = this.calculations$() ?? [];
      this.calculations.set(calculations);
    });

    // Cargar cálculos al inicializar
    this.loadCalculations();
  }

  loadCalculations(): void {
    // Carga todos los cálculos desde el almacenamiento
    try {
      this.historyError = null;
      this.historySuccess = null;
      this.isLoading.set(true);
      this.storageService.loadCalculations()
        .pipe(
          catchError(error => {
            this.historyError = 'Error al cargar el historial.';
            this.showError('Error al cargar el historial');
            return EMPTY;
          }),
          finalize(() => {
            this.isLoading.set(false);
          })
        )
        .subscribe({
          next: (calculations) => {
            try {
              this.calculations.set(calculations);
              this.historySuccess = 'Historial cargado correctamente.';
            } catch (error) {
              this.historyError = 'Error al procesar los datos.';
              this.showError('Error al procesar los datos');
            }
          },
          error: (error) => {
            this.historyError = 'Error al cargar los datos.';
            this.showError('Error al cargar los datos');
          }
        });
    } catch (error) {
      this.historyError = 'Error inesperado al cargar el historial.';
      this.showError('Error inesperado al cargar el historial');
      this.isLoading.set(false);
    }
  }

  clearHistory(): void {
    // Elimina todo el historial de cálculos
    try {
      this.historyError = null;
      this.historySuccess = null;
      const confirmMessage = '¿Estás seguro de que quieres eliminar todo el historial? Esta acción no se puede deshacer.';
      if (confirm(confirmMessage)) {
        this.isLoading.set(true);
        this.storageService.clearCalculations()
          .pipe(
            catchError(error => {
              this.historyError = 'Error al limpiar el historial.';
              this.showError('Error al limpiar el historial');
              return EMPTY;
            }),
            finalize(() => {
              this.isLoading.set(false);
            })
          )
          .subscribe({
            next: () => {
              this.calculations.set([]);
              this.historySuccess = 'Historial limpiado correctamente.';
            },
            error: (error) => {
              this.historyError = 'Error durante la limpieza.';
              this.showError('Error durante la limpieza');
            }
          });
      }
    } catch (error) {
      this.historyError = 'Error inesperado al limpiar el historial.';
      this.showError('Error inesperado al limpiar el historial');
      this.isLoading.set(false);
    }
  }

  deleteCalculation(id: string): void {
    // Elimina un cálculo específico del historial
    try {
      this.storageService.deleteCalculation(id)
        .pipe(
          catchError(error => {
            this.showError('Error al eliminar el cálculo');
            return EMPTY;
          })
        )
        .subscribe({
          next: () => {
            this.showSuccess('Cálculo eliminado correctamente');
          },
          error: (error) => {
            this.showError('Error al eliminar el cálculo');
          }
        });
    } catch (error) {
      this.showError('Error inesperado al eliminar el cálculo');
    }
  }

  trackByCalculationId(index: number, calculation: Calculation): string {
    return calculation.id;
  }

  isRecentCalculation(calculation: Calculation): boolean {
    const now = new Date();
    const calculationDate = new Date(calculation.timestamp);
    const timeDiff = now.getTime() - calculationDate.getTime();
    const hoursDiff = timeDiff / (1000 * 3600);
    return hoursDiff < 24;
  }

  navigateToCalculator(): void {
    // Navega de vuelta a la calculadora
    try {
      this.router.navigate(['/']);
    } catch (error) {
      this.showError('Error al navegar a la calculadora');
    }
  }

  formatDate(date: Date): string {
    try {
      return new Intl.DateTimeFormat('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      }).format(new Date(date));
    } catch (error) {
      return 'Fecha inválida';
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