import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { MainContentComponent } from './main-content/main-content.component';
import { ChatComponent } from './chat/chat.component';

import { HttpClientModule } from '@angular/common/http';
import { BusinessDomainDetailsComponent } from './business-domain-details/business-domain-details.component';
import { DatasetDetailsComponent } from './dataset-details/dataset-details.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SidebarComponent,
    MainContentComponent,
    ChatComponent,
    BusinessDomainDetailsComponent,
    DatasetDetailsComponent
  ],
  imports: [
    HttpClientModule,
    FormsModule,
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
