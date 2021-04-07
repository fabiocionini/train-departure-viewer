import { NgModule } from '@angular/core';
import { PagesComponent } from './pages.component';
import { PagesRoutingModule } from './pages-routing.module';
import {CommonModule} from '@angular/common';
import {BrowserModule} from '@angular/platform-browser';
import {HomeComponent} from './home/home.component';

@NgModule({
  imports: [
    CommonModule,
    PagesRoutingModule,
  ],
  declarations: [
    PagesComponent,
    HomeComponent
  ],
  providers: []
})
export class PagesModule {
}
