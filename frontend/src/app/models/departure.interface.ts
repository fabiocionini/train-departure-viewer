export interface Departure {
  id: number,
  name: string,
  planned_time: Date,
  direction: string,
  platform: string,
  train_type: string,
  station: number
}
