import { HttpInterceptorFn } from '@angular/common/http';

export const httpClientInterceptor: HttpInterceptorFn = (req, next) => {
  const clonedRequest = req.clone({ withCredentials: false });
  return next(clonedRequest);
};
