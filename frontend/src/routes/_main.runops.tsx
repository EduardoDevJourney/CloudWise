import { createFileRoute } from '@tanstack/react-router';

import { runopsRequestsQuery } from '@core/queries';
import { ProvisionForm } from '@features/runops/provision-form';
import { RequestList } from '@features/runops/request-list';

export const Route = createFileRoute('/_main/runops')({
  loader: ({ context }) => context.queryClient.ensureQueryData(runopsRequestsQuery),
  component: RunOpsPage,
});

function RunOpsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">RunOps</h1>
      <ProvisionForm />
      <div>
        <h2 className="mb-3 text-lg font-semibold">Solicitações</h2>
        <RequestList />
      </div>
    </div>
  );
}
