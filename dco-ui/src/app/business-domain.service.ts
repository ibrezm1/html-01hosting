import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';  // Ensure correct path to environment

@Injectable({
  providedIn: 'root',
})
export class BusinessDomainService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Method to get business domains, filtered by name if searchTerm is provided
  getBusinessDomains(searchTerm?: string): Observable<any[]> {
    let params = new HttpParams();
    if (searchTerm) {
      params = params.set('name', searchTerm);
    }
    return this.http.get<any[]>(`${this.apiUrl}/business_domain`, { params, withCredentials: true });
  }

  // Method to get domain details by ID
  getDomainDetails(domainId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/business_domain/${domainId}`, { withCredentials: true });
  }

  // Method to get datasets for a domain by ID
  getDatasetsForDomain(domainId: number, searchTerm?: string): Observable<any[]> {
    let params = new HttpParams();
    if (searchTerm) {
      params = params.set('name', searchTerm);
    }
    return this.http.get<any[]>(`${this.apiUrl}/business_domain/${domainId}/dataset`, { params, withCredentials: true });
  }

  // Method to get dataset details by ID
  getDatasetDetails(domainId: number, datasetId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/business_domain/${domainId}/dataset/${datasetId}`, { withCredentials: true });
  }

  // Method to get data assets for a dataset
  getDataAssetsForDataset(domainId: number, datasetId: number, searchTerm?: string): Observable<any[]> {
    let params = new HttpParams();
    if (searchTerm) {
      params = params.set('name', searchTerm);
    }
    return this.http.get<any[]>(`${this.apiUrl}/business_domain/${domainId}/dataset/${datasetId}/data_asset`, { params, withCredentials: true });
  }

  // Method to get data asset details by ID
  getDataAssetDetails(domainId: number, datasetId: number, dataAssetId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/business_domain/${domainId}/dataset/${datasetId}/data_asset/${dataAssetId}`, { withCredentials: true });
  }

  // Method to get columns for a data asset
  getColumnsForDataAsset(domainId: number, datasetId: number, dataAssetId: number, searchTerm?: string): Observable<any[]> {
    let params = new HttpParams();
    if (searchTerm) {
      params = params.set('name', searchTerm);
    }
    return this.http.get<any[]>(`${this.apiUrl}/business_domain/${domainId}/dataset/${datasetId}/data_asset/${dataAssetId}/column`, { params, withCredentials: true });
  }

  // Method to get column details by ID
  getColumnDetails(domainId: number, datasetId: number, dataAssetId: number, columnId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/business_domain/${domainId}/dataset/${datasetId}/data_asset/${dataAssetId}/column/${columnId}`, { withCredentials: true });
  }
}