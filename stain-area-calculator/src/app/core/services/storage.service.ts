import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, throwError, catchError, tap } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Calculation } from '../models/calculation.model';

@Injectable({
  providedIn: 'root'
})
export class StorageService {
  private readonly STORAGE_KEY = 'stain_calculations';
  private readonly calculationsSubject = new BehaviorSubject<Calculation[]>([]);

  readonly calculations$: Observable<Calculation[]> = this.calculationsSubject.asObservable();

  constructor(private snackBar: MatSnackBar) {
    if (this.isBrowser()) {
      this.loadCalculations().subscribe();
    }
  }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && !!window.localStorage;
  }

  // Guarda un cálculo en localStorage y actualiza el estado
  saveCalculation(calculation: Calculation): Observable<void> {
    return new Observable<void>(observer => {
      try {
        if (!this.isBrowser()) {
          observer.next();
          observer.complete();
          return;
        }

        const calculations = this.calculationsSubject.value;
        const updatedCalculations = [calculation, ...calculations];

        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updatedCalculations));
        this.calculationsSubject.next(updatedCalculations);

        observer.next();
        observer.complete();
      } catch (error) {
        observer.error(error);
      }
    }).pipe(
      tap(() => {
        this.showSuccess('Cálculo guardado exitosamente');
      }),
      catchError((error: unknown) => {
        this.showError('Error al guardar el cálculo');
        return throwError(() => error);
      })
    );
  }

  // Carga todos los cálculos desde localStorage
  loadCalculations(): Observable<Calculation[]> {
    return new Observable<Calculation[]>(observer => {
      try {
        if (!this.isBrowser()) {
          this.calculationsSubject.next([]);
          observer.next([]);
          observer.complete();
          return;
        }

        const storedData = localStorage.getItem(this.STORAGE_KEY);

        if (!storedData) {
          this.calculationsSubject.next([]);
          observer.next([]);
          observer.complete();
          return;
        }

        const calculations: Calculation[] = JSON.parse(storedData);

        // Validar y convertir las fechas
        const validCalculations = calculations.map(calc => ({
          ...calc,
          timestamp: new Date(calc.timestamp)
        }));

        this.calculationsSubject.next(validCalculations);

        observer.next(validCalculations);
        observer.complete();
      } catch (error) {
        observer.error(error);
      }
    }).pipe(
      catchError((error: unknown) => {
        this.showError('Error al cargar los cálculos');
        return throwError(() => error);
      })
    );
  }

  // Elimina todos los cálculos del almacenamiento
  clearCalculations(): Observable<void> {
    return new Observable<void>(observer => {
      try {
        if (!this.isBrowser()) {
          this.calculationsSubject.next([]);
          observer.next();
          observer.complete();
          return;
        }

        localStorage.removeItem(this.STORAGE_KEY);
        this.calculationsSubject.next([]);

        observer.next();
        observer.complete();
      } catch (error) {
        observer.error(error);
      }
    }).pipe(
      tap(() => {
        this.showSuccess('Historial limpiado exitosamente');
      }),
      catchError((error: unknown) => {
        this.showError('Error al limpiar el historial');
        return throwError(() => error);
      })
    );
  }

  // Elimina un cálculo específico por ID
  deleteCalculation(id: string): Observable<void> {
    return new Observable<void>(observer => {
      try {
        if (!this.isBrowser()) {
          observer.next();
          observer.complete();
          return;
        }

        const calculations = this.calculationsSubject.value;
        const filteredCalculations = calculations.filter(calc => calc.id !== id);

        if (filteredCalculations.length === calculations.length) {
          observer.error(new Error('Cálculo no encontrado'));
          return;
        }

        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(filteredCalculations));
        this.calculationsSubject.next(filteredCalculations);

        observer.next();
        observer.complete();
      } catch (error) {
        observer.error(error);
      }
    }).pipe(
      tap(() => {
        this.showSuccess('Cálculo eliminado exitosamente');
      }),
      catchError((error: unknown) => {
        this.showError('Error al eliminar el cálculo');
        return throwError(() => error);
      })
    );
  }

  getCalculations(): Calculation[] {
    try {
      return this.calculationsSubject.value;
    } catch (error) {
      return [];
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
