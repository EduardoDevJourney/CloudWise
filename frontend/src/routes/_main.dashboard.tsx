import { createFileRoute } from '@tanstack/react-router';

import { cloudWiseDashboardQuery } from '@core/queries';
import { CloudWiseDashboard } from '@features/cloudwise/dashboard';

export const Route = createFileRoute('/_main/dashboard')({
  loader: ({ context }) => context.queryClient.ensureQueryData(cloudWiseDashboardQuery()),
  component: DashboardPage,
});

function DashboardPage() {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-2xl font-bold text-slate-900">Cloud Wise Dashboard</h1>
        <span
          data-testid="sample-data-badge"
          title="Made-up costs used for demonstration"
          className="rounded-full border border-amber-300 bg-amber-50 px-2.5 py-0.5 text-xs font-medium text-amber-800"
        >
          Sample data
        </span>
      </div>
      <CloudWiseDashboard />
    </div>
  );
}
