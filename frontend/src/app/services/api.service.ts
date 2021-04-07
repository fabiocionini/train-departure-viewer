import { Injectable } from '@angular/core';
import {environment} from '../../environments/environment'
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  public readonly endpoint: string;

  constructor(private http: HttpClient) {
    this.endpoint = environment.rootUrl + environment.apiPrefix
  }

  private headers(): HttpHeaders {
    const headers = new HttpHeaders()
    headers.set('Accept', `${environment.apiMimeType}; version=${environment.apiVersion}`)
    if (environment.apiAuthorization) {
      headers.set('X-Api-Key', environment.apiKey)
    }
    return headers
  }

  private httpGetObservable(api: string, params: any = {}): Observable<any> {
    let url = ''
    if (params.raw) {
      url = api
    }
    else {
      url = this.endpoint + api
    }

    const headers = this.headers()

    const options: any = {headers}
    if (params.responseType) {
      options.responseType = params.responseType
    }
    if (params.observe) {
      options.observe = params.observe
    }

    return this.http.get<unknown>(url, options).pipe(catchError(er => {
      return throwError(er)
    }))
  }

  private httpGetPromise(api: string, params?: unknown): Promise<any> {
    return this.httpGetObservable(api, params).toPromise()
  }

  public getStation(): Promise<any> {
    return this.httpGetPromise('stations/').then(res => res.length > 0 ? res[0] : null)
  }

  public getDepartures(): Promise<any> {
    return this.httpGetPromise('departures/')
  }
}
