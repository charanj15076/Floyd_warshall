import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

import * as L from "leaflet";
 
export interface GetResult {
  data: any[];
  status: string;
}

export interface PostResult {
  message: string;
  id: number;
  lat: number;
  lng: number;
  status: string;
}
 
@Injectable({
  providedIn: 'root',
})

export class BlockageService {
  constructor(private http: HttpClient) {}
 
  // get all blockages within a certain boundary rectangle
  getBlockages(bounds: L.LatLngBounds): Observable<GetResult> {
    const params = new HttpParams({
      fromObject: {
        xmin: bounds.getSouthWest().lng,
        ymin: bounds.getSouthWest().lat,
        xmax: bounds.getNorthEast().lng,
        ymax: bounds.getNorthEast().lat,
      }
    });

    return this.http.get<GetResult>(
      `${environment.baseUrl}/blockages`,
      { params: params }
    );
  }

  // add a blockage
  postBlockage(postData: any): Observable<PostResult> {
    return this.http.post<PostResult>(
      `${environment.baseUrl}/blockages`,
      { 
        lat: postData.lat,
        lng: postData.lng,
      }
    );
  }
 
  // remove a blockage
  deleteBlockage(deleteId: number): Observable<ArrayBuffer> {
    const httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' }), 
        body: { 
          'id': deleteId
        }
    };
    return this.http.delete<ArrayBuffer>(
      `${environment.baseUrl}/blockages`,
      httpOptions
    );
  }
}