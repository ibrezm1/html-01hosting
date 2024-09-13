import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BusinessDomainService } from '../business-domain.service';
import { Observable, Subject, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, catchError } from 'rxjs/operators';

interface DomainDetails {
  name: string;
  description: string;
  db_name: string;
  custom_fields?: Record<string, any>;
}

interface Dataset {
  id: number;
  name: string;
  description: string;
  owner: string;
  last_updated: string;
}

@Component({
  selector: 'app-business-domain-details',
  templateUrl: './business-domain-details.component.html',
  styleUrls: ['./business-domain-details.component.css']
})
export class BusinessDomainDetailsComponent implements OnInit {
  domainId: number = 0;
  domainDetails$: Observable<DomainDetails> = of({} as DomainDetails);
  datasets$: Observable<Dataset[]> = of([]);
  private searchTerms = new Subject<string>();

  constructor(
    private route: ActivatedRoute,
    private businessDomainService: BusinessDomainService
  ) {}

  ngOnInit() {
    // Subscribe to paramMap to detect changes in route parameters
    this.route.paramMap.subscribe(paramMap => {
      const id = paramMap.get('id');
      if (id !== null) {
        this.domainId = +id;
        this.getDomainDetails();
        this.getDatasets();
      } else {
        console.error('No domain ID provided');
        // Handle error, e.g., redirect to a 404 page or show an error message
      }
    });

    // Stream to handle dataset search input with debouncing
    this.datasets$ = this.searchTerms.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap((term: string) =>
        this.businessDomainService.getDatasetsForDomain(this.domainId, term).pipe(
          catchError(error => {
            console.error('Error fetching datasets:', error);
            return of([]);
          })
        )
      )
    );
  }

  // Fetch business domain details
  getDomainDetails() {
    this.domainDetails$ = this.businessDomainService.getDomainDetails(this.domainId).pipe(
      catchError(error => {
        console.error('Error fetching domain details:', error);
        return of({} as DomainDetails);
      })
    );
  }

  // Fetch datasets related to the domain
  getDatasets() {
    this.searchDatasets(''); // Trigger an initial search with an empty string
  }

  // Trigger a dataset search based on the search term
  searchDatasets(term: string): void {
    this.searchTerms.next(term);
  }
}
