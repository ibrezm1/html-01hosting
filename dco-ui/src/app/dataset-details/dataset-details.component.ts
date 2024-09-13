import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BusinessDomainService } from '../business-domain.service';
import { Observable, Subject, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, catchError } from 'rxjs/operators';

interface data_asset {
  name: string;
  description: string;
  owner: string;
  last_updated: string;
}

interface Dataset {
  id: number;
  name: string;
  description: string;
  owner: string;
  last_updated: string;
}

@Component({
  selector: 'app-dataset-details',
  templateUrl: './dataset-details.component.html',
  styleUrls: ['./dataset-details.component.css']
})
export class DatasetDetailsComponent {

}
