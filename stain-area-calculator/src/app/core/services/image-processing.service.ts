import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, throwError, catchError, tap } from 'rxjs';
import { Point, ImageSize } from '../interfaces/app.interfaces';

@Injectable({
  providedIn: 'root'
})
export class ImageProcessingService {
  private canvas: HTMLCanvasElement | null = null;
  private ctx: CanvasRenderingContext2D | null = null;
  private imageData: ImageData | null = null;

  private readonly imageLoadedSubject = new BehaviorSubject<boolean>(false);
  private readonly imageDimensionsSubject = new BehaviorSubject<ImageSize>({ width: 0, height: 0 });

  readonly imageLoaded$: Observable<boolean> = this.imageLoadedSubject.asObservable();
  readonly imageDimensions$: Observable<ImageSize> = this.imageDimensionsSubject.asObservable();

  // Método principal para cargar y procesar una imagen
  // Convierte la imagen a un canvas para análisis de píxeles
  loadImage(image: File): Observable<void> {
    return new Observable<void>(observer => {
      try {
        const reader = new FileReader();

        reader.onload = (event) => {
          try {
            const img = new Image();

            img.onload = () => {
              try {
                this.canvas = document.createElement('canvas');
                this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });

                if (!this.ctx) {
                  const error = new Error('No se pudo obtener el contexto del canvas');
                  observer.error(error);
                  return;
                }

                this.canvas.width = img.width;
                this.canvas.height = img.height;
                this.imageDimensionsSubject.next({ width: img.width, height: img.height });
                this.ctx.drawImage(img, 0, 0);
                this.imageData = this.ctx.getImageData(0, 0, img.width, img.height);

                this.imageLoadedSubject.next(true);
                observer.next();
                observer.complete();
              } catch (error) {
                observer.error(error);
              }
            };

            img.onerror = (error) => {
              observer.error(new Error('Error al cargar la imagen'));
            };

            img.src = event.target?.result as string;
          } catch (error) {
            observer.error(error);
          }
        };

        reader.onerror = (error) => {
          observer.error(new Error('Error al leer el archivo'));
        };

        reader.readAsDataURL(image);
      } catch (error) {
        observer.error(error);
      }
    }).pipe(
      catchError((error: unknown) => {
        this.imageLoadedSubject.next(false);
        return throwError(() => error);
      })
    );
  }

  isPointInStain(x: number, y: number): boolean {
    try {
      if (!this.imageData || !this.ctx) {
        return false;
      }

      const pixelIndex = (y * this.imageData.width + x) * 4;

      if (pixelIndex < 0 || pixelIndex >= this.imageData.data.length) {
        return false;
      }

      // En una imagen binaria, los píxeles blancos tienen R=255, G=255, B=255
      return (
        this.imageData.data[pixelIndex] === 255 &&
        this.imageData.data[pixelIndex + 1] === 255 &&
        this.imageData.data[pixelIndex + 2] === 255
      );
    } catch (error) {
      return false;
    }
  }

  countPointsInStain(points: Point[]): number {
    try {
      if (!points || points.length === 0) {
        return 0;
      }

      const pointsInStain = points.filter(point => this.isPointInStain(point.x, point.y)).length;
      return pointsInStain;
    } catch (error) {
      return 0;
    }
  }

  getCanvas(): HTMLCanvasElement | null {
    return this.canvas;
  }

  getCurrentImageUrl(): string | null {
    try {
      if (!this.canvas) {
        return null;
      }
      return this.canvas.toDataURL();
    } catch (error) {
      return null;
    }
  }

  clearImage(): void {
    try {
      this.canvas = null;
      this.ctx = null;
      this.imageData = null;
      this.imageLoadedSubject.next(false);
      this.imageDimensionsSubject.next({ width: 0, height: 0 });
    } catch (error) {
    }
  }
}
