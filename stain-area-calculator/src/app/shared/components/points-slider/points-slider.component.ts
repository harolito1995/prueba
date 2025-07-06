import { Component, EventEmitter, Input, Output, signal, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatSliderModule } from '@angular/material/slider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-points-slider',
  standalone: true,
  imports: [CommonModule, FormsModule, MatCardModule, MatSliderModule, MatFormFieldModule, MatInputModule, MatChipsModule, MatIconModule],
  templateUrl: './points-slider.component.html',
  styleUrls: ['./points-slider.component.scss']
})
export class PointsSliderComponent {
  @Input() min = 100;
  @Input() max = 10000;
  @Input() step = 100;
  @Input() value = 1000;
  @Input() disabled = false;
  @Output() valueChanged = new EventEmitter<number>();

  // Signal para el valor actual
  readonly points = signal(1000);

  // Computed para validar el rango
  readonly isValidRange = computed(() => {
    const currentValue = this.points();
    return currentValue >= this.min && currentValue <= this.max;
  });

  constructor() {
    // Effect para sincronizar el valor inicial
    effect(() => {
      this.points.set(this.value);
    });
  }

  onChange(value: number): void {
    if (this.disabled) return;
    
    this.points.set(value);
    this.valueChanged.emit(value);
  }

  onSliderChange(event: any): void {
    const value = typeof event === 'number' ? event : event.target?.value || event;
    this.onChange(value);
  }

  onInputChange(event: any): void {
    const value = parseInt(event.target.value, 10);
    if (!isNaN(value) && value >= this.min && value <= this.max) {
      this.onChange(value);
    }
  }
} 