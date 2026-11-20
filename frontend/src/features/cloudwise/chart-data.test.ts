import { describe, expect, it } from 'vitest';

import type { CostSeriesDay } from '@core/types/api';
import { shortDate, shortService, toDailyPoints, toServicePoints } from '@features/cloudwise/chart-data';

const series: CostSeriesDay[] = [
  { date: '2026-06-01', total_cost: 125.5, by_service: { 'Microsoft.Storage': 100, 'Microsoft.Compute': 25.5 } },
  { date: '2026-06-02', total_cost: 89.333, by_service: { 'Microsoft.Compute': 89.333 } },
];

describe('chart-data', () => {
  it('builds the rounded daily series', () => {
    expect(toDailyPoints(series)).toEqual([
      { date: '2026-06-01', total: 125.5 },
      { date: '2026-06-02', total: 89.33 },
    ]);
  });

  it('sums per service in descending order', () => {
    expect(toServicePoints(series)).toEqual([
      { service: 'Microsoft.Compute', total: 114.83 },
      { service: 'Microsoft.Storage', total: 100 },
    ]);
  });

  it('formats labels', () => {
    expect(shortDate('2026-06-01')).toBe('01/06');
    expect(shortService('Microsoft.Storage')).toBe('Storage');
  });

  it('handles an empty series', () => {
    expect(toDailyPoints([])).toEqual([]);
    expect(toServicePoints([])).toEqual([]);
  });
});
