import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainContentComponent } from './main-content/main-content.component';
import { BusinessDomainDetailsComponent } from './business-domain-details/business-domain-details.component';

const routes: Routes = [
  {path: '', component: MainContentComponent},
  { path: 'business-domain/:id', component: BusinessDomainDetailsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
