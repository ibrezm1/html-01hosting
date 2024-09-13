import { Component, OnInit } from '@angular/core';
import { BusinessDomainService } from '../business-domain.service';


@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  searchTerm: string = '';  // Model to bind to the input field
  businessDomains: any[] = [];  // To store the business domains

  constructor(private businessDomainService: BusinessDomainService) {}

  ngOnInit(): void {
    // Initial load of all domains
    this.loadDomains();
  }

  // Method to load all domains or search based on input
  loadDomains(): void {
    this.businessDomainService.getBusinessDomains(this.searchTerm).subscribe(
      (domains) => {
        this.businessDomains = domains;
      },
      (error) => {
        console.error('Error fetching business domains:', error);
      }
    );
  }

  // Method triggered when search input changes
  searchDomains(): void {
    this.loadDomains();
  }
}
