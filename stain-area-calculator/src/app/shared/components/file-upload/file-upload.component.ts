import { Component, EventEmitter, Output, signal, Input, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FilePreviewPipe } from '../../pipes/file-preview.pipe';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule, FormsModule, MatCardModule, MatButtonModule, MatIconModule, FilePreviewPipe],
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})
export class FileUploadComponent {
  @Input() disabled = false;
  @Output() fileSelected = new EventEmitter<File>();
  
  // Signals para estado reactivo
  readonly uploadedFile = signal<File | null>(null);
  readonly isDragOver = signal(false);

  // Computed para validar el archivo
  readonly isValidFile = computed(() => {
    const file = this.uploadedFile();
    return file && file.type.startsWith('image/');
  });

  // Variables para mensajes
  uploadError: string | null = null;
  uploadSuccess: string | null = null;

  onFileSelect(event: any): void {
    if (this.disabled) return;
    this.uploadError = null;
    this.uploadSuccess = null;
    const file = event.target.files[0];
    if (file) {
      this.processFile(file);
    }
  }

  onDragOver(event: DragEvent): void {
    if (this.disabled) return;
    
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver.set(true);
  }

  onDragLeave(event: DragEvent): void {
    if (this.disabled) return;
    
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver.set(false);
  }

  onDrop(event: DragEvent): void {
    if (this.disabled) return;
    this.uploadError = null;
    this.uploadSuccess = null;
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver.set(false);
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      const file = files[0];
      this.processFile(file);
    }
  }

  clear(): void {
    if (this.disabled) return;
    this.uploadedFile.set(null);
    this.uploadError = null;
    this.uploadSuccess = null;
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  private processFile(file: File): void {
    if (!file.type.startsWith('image/')) {
      this.uploadError = 'El archivo seleccionado no es una imagen válida.';
      this.uploadedFile.set(null);
      return;
    }
    
    console.log('📁 Archivo procesado:', file.name);
    this.uploadedFile.set(file);
    this.fileSelected.emit(file);
    this.uploadSuccess = 'Imagen cargada correctamente.';
  }
} 