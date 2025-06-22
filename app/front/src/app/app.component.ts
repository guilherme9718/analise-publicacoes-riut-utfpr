import { Component, inject, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { NavbarComponent } from './components/navbar/navbar.component';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    ButtonModule,
    NavbarComponent,
    CommonModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  router = inject(Router);

  ngOnInit() {

  }
}
