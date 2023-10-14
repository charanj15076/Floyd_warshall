import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

import * as L from "leaflet";
 
export interface GetResult {
  data: any;
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class RoutesService {
  constructor(private http: HttpClient) {}
 
  // get all blockages within a certain boundary rectangle
  getRoutes(source: L.LatLng, destination: L.LatLng): Observable<GetResult> {
    const params = new HttpParams({
      fromObject: {
        source_lng: source.lng,
        source_lat: source.lat,
        destination_lng: destination.lng,
        destination_lat: destination.lat,
      }
    });

    return this.http.get<GetResult>(
      `${environment.baseUrl}/routes`,
      { params: params }
    );
  }
}
