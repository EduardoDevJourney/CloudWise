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
      <h1 className="text-2xl font-bold text-slate-900">Cloud Wise Dashboard</h1>
      <CloudWiseDashboard />
    </div>
  );
}
