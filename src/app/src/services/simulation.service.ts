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
  providedIn: 'root',
})

export class SimulationService {
  constructor(private http: HttpClient) {}
 
  // get all blockages within a certain boundary rectangle
  getSimulation(source: L.LatLng, distance: number): Observable<GetResult> {
    const params = new HttpParams({
      fromObject: {
        source_lng: source.lng,
        source_lat: source.lat,
        distance: distance,
      }
    });

    return this.http.get<GetResult>(
      `${environment.baseUrl}/simulate`,
      { params: params }
    );
  }
}