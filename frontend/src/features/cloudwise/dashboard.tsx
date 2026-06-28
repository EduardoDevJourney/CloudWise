import { useQuery } from '@tanstack/react-query';

import { cloudWiseDashboardQuery } from '@core/queries';
import { Loading } from '@ui/loading';

export function CloudWiseDashboard() {
  const { data, isLoading, isError, error } = useQuery(cloudWiseDashboardQuery);

  if (isLoading) return <Loading label="Carregando dashboard..." />;
  if (isError) return <p className="text-sm text-red-600">{(error as Error).message}</p>;
  if (!data) return <p className="text-sm text-slate-500">Sem dados disponíveis.</p>;

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-3">
        <article className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Custo total</p>
          <p className="text-2xl font-semibold">${data.summary.total_cost.toFixed(2)}</p>
        </article>
        <article className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Top serviço</p>
          <p className="text-2xl font-semibold">{data.summary.top_service}</p>
        </article>
        <article className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-sm text-slate-500">Subscriptions</p>
          <p className="text-2xl font-semibold">{data.summary.subscription_count}</p>
        </article>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold">Série diária</h2>
        <div className="space-y-2">
          {data.series.map((day) => (
            <div key={day.date} className="flex items-center justify-between text-sm">
              <span>{day.date}</span>
              <span className="font-medium">${day.total_cost.toFixed(2)}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
