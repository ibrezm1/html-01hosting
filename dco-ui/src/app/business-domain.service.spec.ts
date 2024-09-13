import { TestBed } from '@angular/core/testing';

import { BusinessDomainService } from './business-domain.service';

describe('BusinessDomainService', () => {
  let service: BusinessDomainService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BusinessDomainService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
