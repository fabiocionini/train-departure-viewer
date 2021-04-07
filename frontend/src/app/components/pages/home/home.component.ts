import {Component, Inject, OnDestroy, OnInit} from '@angular/core';
import {ApiService} from '../../../services/api.service';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';
import {Station} from '../../../models/station.interface';
import {Departure} from '../../../models/departure.interface';
import {interval, Subscription} from 'rxjs';
import {environment} from '../../../../environments/environment';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  station: Station | undefined
  departures: Departure[] = []
  currentDate: Date | undefined
  currentPage = 1

  trainTypes = [
    {
      type: 'IC',
      name: 'InterCity'
    },
    {
      type: 'SPR',
      name: 'Sprinter'
    }
  ]

  updateIntervalSubscription: Subscription | undefined
  cycleIntervalSubscription: Subscription | undefined
  dateIntervalSubscription: Subscription | undefined

  constructor(private api: ApiService, @Inject(PLATFORM_ID) private platformId: any | undefined) {

  }

  ngOnInit(): void {
    // first update happens always (SSR and browser)
    this.updateCurrentDate()
    this.updateStation().then(() => {
      this.updateDepartures()
    })
    if (isPlatformBrowser(this.platformId)) {
      // periodical updates happen only on browser
      const source = interval(environment.refreshDataRate * 1000)
      this.updateIntervalSubscription = source.subscribe(next => this.updateDepartures())

      const dateSource = interval(1000)
      this.dateIntervalSubscription = dateSource.subscribe(next => this.updateCurrentDate())

      const refreshSource = interval(environment.pageCycleRate * 1000)
      this.cycleIntervalSubscription = refreshSource.subscribe(next => this.cyclePage())
    }
  }

  cyclePage(): void {
    this.currentPage += 1
    if (this.currentPage > this.totalPages) {
      this.currentPage = 1
    }
  }

  updateCurrentDate(): void {
    this.currentDate = new Date()
  }

  get totalPages(): number {
    return Math.ceil(this.departures.length / environment.departuresPerPage)
  }

  get paginatedDepartures(): Departure[] {
    const start = (this.currentPage - 1) * environment.departuresPerPage
    const end = start + environment.departuresPerPage
    return this.departures.slice(start, end)
  }

  async updateStation(): Promise<void> {
    this.station = await this.api.getStation()
  }

  async updateDepartures(): Promise<void> {
    const data = await this.api.getDepartures()
    if (data) {
      this.departures = data.filter((d: { planned_time: string | number | Date; }) => {
        return new Date(d.planned_time) >= new Date()
      })
    }
  }

  isBoarding(time: Date): boolean {
    const date = new Date(time)
    return (date.getTime() - Date.now()) / 1000 < environment.boardingTime
  }

  get stationName(): string | null {
    return this.station?.name || null
  }

  getTrainType(type: string): string {
    return this.trainTypes.find(t => t.type === type)?.name || type
  }

  ngOnDestroy(): void {
    if (this.updateIntervalSubscription) {
      this.updateIntervalSubscription.unsubscribe()
    }
    if (this.cycleIntervalSubscription) {
      this.cycleIntervalSubscription.unsubscribe()
    }
    if (this.dateIntervalSubscription) {
      this.dateIntervalSubscription.unsubscribe()
    }
  }
}
