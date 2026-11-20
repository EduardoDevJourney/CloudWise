import type { CostSeriesDay } from '@core/types/api';

export type DailyPoint = { date: string; total: number };
export type ServicePoint = { service: string; total: number };

const round = (value: number) => Math.round(value * 100) / 100;

export function toDailyPoints(series: CostSeriesDay[]): DailyPoint[] {
  return series.map((day) => ({ date: day.date, total: round(day.total_cost) }));
}

export function toServicePoints(series: CostSeriesDay[]): ServicePoint[] {
  const totals = new Map<string, number>();
  for (const day of series) {
    for (const [service, cost] of Object.entries(day.by_service)) {
      totals.set(service, (totals.get(service) ?? 0) + cost);
    }
  }
  return [...totals.entries()]
    .map(([service, total]) => ({ service, total: round(total) }))
    .sort((a, b) => b.total - a.total);
}

export function shortDate(iso: string): string {
  const [, month, day] = iso.split('-');
  return `${day}/${month}`;
}

export function shortService(name: string): string {
  return name.replace(/^Microsoft\./, '');
}
