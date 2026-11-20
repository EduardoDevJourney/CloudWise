import { useQuery } from '@tanstack/react-query';
import { useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import { describeError } from '@core/errors';
import { cloudWiseCostsQuery, cloudWiseDashboardQuery } from '@core/queries';
import type { CostFilters } from '@core/types/api';
import { Button } from '@ui/button';
import { Input } from '@ui/input';
import { Loading } from '@ui/loading';
import { Select } from '@ui/select';
import {
  shortDate,
  shortService,
  toDailyPoints,
  toServicePoints,
} from '@features/cloudwise/chart-data';

const usd = (value: number) => `$${value.toFixed(2)}`;

const card = 'rounded-lg border border-slate-200 bg-white p-4 shadow-sm';

export function CloudWiseDashboard() {
  const [filters, setFilters] = useState<CostFilters>({});
  const { data, isLoading, isError, error } = useQuery(cloudWiseDashboardQuery(filters));
  // filter options come from the full, unfiltered cost list
  const { data: allCosts } = useQuery(cloudWiseCostsQuery());

  const services = useMemo(
    () => [...new Set((allCosts ?? []).map((c) => c.resource_type))].sort(),
    [allCosts],
  );
  const subscriptions = useMemo(
    () => [...new Set((allCosts ?? []).map((c) => c.subscription_id))].sort(),
    [allCosts],
  );

  const setFilter = (key: keyof CostFilters, value: string) =>
    setFilters((current) => ({ ...current, [key]: value || undefined }));

  return (
    <div className="space-y-6">
      <section aria-label="Filters" className={`grid gap-3 md:grid-cols-5 ${card}`}>
        <label className="space-y-1 text-sm">
          <span>Service</span>
          <Select value={filters.service ?? ''} onChange={(e) => setFilter('service', e.target.value)}>
            <option value="">All</option>
            {services.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </Select>
        </label>
        <label className="space-y-1 text-sm">
          <span>Subscription</span>
          <Select
            value={filters.subscription_id ?? ''}
            onChange={(e) => setFilter('subscription_id', e.target.value)}
          >
            <option value="">All</option>
            {subscriptions.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </Select>
        </label>
        <label className="space-y-1 text-sm">
          <span>From</span>
          <Input type="date" value={filters.start ?? ''} onChange={(e) => setFilter('start', e.target.value)} />
        </label>
        <label className="space-y-1 text-sm">
          <span>To</span>
          <Input type="date" value={filters.end ?? ''} onChange={(e) => setFilter('end', e.target.value)} />
        </label>
        <div className="flex items-end">
          <Button variant="secondary" onClick={() => setFilters({})}>
            Clear filters
          </Button>
        </div>
      </section>

      {isLoading ? <Loading label="Loading dashboard..." /> : null}
      {isError ? <p className="text-sm text-red-600">{describeError(error)}</p> : null}
      {data ? (
        <>
          <section className="grid gap-4 md:grid-cols-3">
            <article className={card}>
              <p className="text-sm text-slate-500">Total cost</p>
              <p className="text-2xl font-semibold">{usd(data.summary.total_cost)}</p>
            </article>
            <article className={card}>
              <p className="text-sm text-slate-500">Top service</p>
              <p className="text-2xl font-semibold">{data.summary.top_service}</p>
            </article>
            <article className={card}>
              <p className="text-sm text-slate-500">Subscriptions</p>
              <p className="text-2xl font-semibold">{data.summary.subscription_count}</p>
            </article>
          </section>

          {data.series.length === 0 ? (
            <p className={`${card} text-sm text-slate-500`}>No data for the selected filters.</p>
          ) : (
            <div className="grid gap-4 lg:grid-cols-2">
              <section className={card}>
                <h2 className="mb-4 text-lg font-semibold">Cost per day</h2>
                <div className="h-64" data-testid="chart-daily">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={toDailyPoints(data.series)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="date" tickFormatter={shortDate} fontSize={12} />
                      <YAxis tickFormatter={usd} fontSize={12} width={64} />
                      <Tooltip formatter={(value) => usd(Number(value))} />
                      <Line type="monotone" dataKey="total" name="Cost" stroke="#2563eb" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </section>

              <section className={card}>
                <h2 className="mb-4 text-lg font-semibold">Cost per service</h2>
                <div className="h-64" data-testid="chart-services">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={toServicePoints(data.series)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="service" tickFormatter={shortService} fontSize={12} />
                      <YAxis tickFormatter={usd} fontSize={12} width={64} />
                      <Tooltip formatter={(value) => usd(Number(value))} />
                      <Bar dataKey="total" name="Cost" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </section>
            </div>
          )}
        </>
      ) : null}
    </div>
  );
}
