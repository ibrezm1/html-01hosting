import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BusinessDomainDetailsComponent } from './business-domain-details.component';

describe('BusinessDomainDetailsComponent', () => {
  let component: BusinessDomainDetailsComponent;
  let fixture: ComponentFixture<BusinessDomainDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BusinessDomainDetailsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BusinessDomainDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
