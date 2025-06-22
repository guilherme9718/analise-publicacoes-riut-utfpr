import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { IconField } from 'primeng/iconfield';
import { InputIcon } from 'primeng/inputicon';
import { InputTextModule } from 'primeng/inputtext';
import { debounceTime } from 'rxjs';
import { SearchService } from '../../services/search.service';
import { TableModule } from 'primeng/table';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'home',
  imports: [
    InputIcon,
    IconField,
    InputTextModule,
    FormsModule,
    ReactiveFormsModule,
    TableModule,
    CommonModule,
    ButtonModule,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent implements OnInit {
  articleService = inject(SearchService);
  formBuilder = inject(FormBuilder);
  form = this.formBuilder.group({
    query: [''],
  });
  articles$ = this.articleService.data$;
  loading$ = this.articleService.loading$;

  ngOnInit(): void {
    this.form
      .get('query')
      ?.valueChanges.pipe(debounceTime(300))
      .subscribe((value) => {
        if (value != null && value != '') this.articleService.fetchData(value);
      });
  }
}
