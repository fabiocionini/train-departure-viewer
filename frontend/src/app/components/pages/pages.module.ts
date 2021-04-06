import { NgModule } from '@angular/core';
import { PagesComponent } from './pages.component';
import { PagesRoutingModule } from './pages-routing.module';

@NgModule({
  imports: [
    PagesRoutingModule,
  ],
  declarations: [
    PagesComponent,
  ],
  providers: []
})
export class PagesModule {
}
