import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { Article } from '../models/article.model';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  http = inject(HttpClient);
  baseApiUrl = environment.baseApiUrl + 'articles';

  private articlesEntries = new BehaviorSubject<Article[]>([]);
  data$: Observable<Article[]> = this.articlesEntries.asObservable();
  loading$ = new BehaviorSubject<boolean>(false);

  fetchData(query: string) {
    let params = new HttpParams();
    params = params.set('query', query);
    this.loading$.next(true);
    return this.http
      .get<Article[]>(this.baseApiUrl, { params })
      .subscribe((data) => {
        this.articlesEntries.next(data);
        this.loading$.next(false);
      });
  }

  getData() {
    return this.data$;
  }
}
