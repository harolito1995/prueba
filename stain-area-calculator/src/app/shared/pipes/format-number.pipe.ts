import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatNumber',
  standalone: true
})
export class FormatNumberPipe implements PipeTransform {
  transform(value: number): string {
    try {
      if (value === null || value === undefined || isNaN(value)) {
        return '0';
      }
      return value.toFixed(2);
    } catch (error) {
      console.error('❌ Error al formatear número:', error);
      return '0';
    }
  }
} 