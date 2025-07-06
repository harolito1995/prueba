import { Routes } from '@angular/router';
import { CalculatorComponent } from './features/calculator/calculator.component';
import { HistoryComponent } from './features/history/history.component';

export const routes: Routes = [
  { path: '', redirectTo: '/calculator', pathMatch: 'full' },
  { path: 'calculator', component: CalculatorComponent },
  { path: 'history', component: HistoryComponent },
  { path: '**', redirectTo: '/calculator' }
];


