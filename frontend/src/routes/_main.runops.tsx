import { createFileRoute } from '@tanstack/react-router';

import { useAuth } from '@core/auth-context';
import { runopsRequestsQuery } from '@core/queries';
import { canProvision } from '@core/roles';
import { ProvisionForm } from '@features/runops/provision-form';
import { RequestList } from '@features/runops/request-list';

export const Route = createFileRoute('/_main/runops')({
  loader: ({ context }) => context.queryClient.ensureQueryData(runopsRequestsQuery),
  component: RunOpsPage,
});

function RunOpsPage() {
  const { role } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">RunOps</h1>
      {canProvision(role) ? (
        <ProvisionForm />
      ) : (
        <p className="rounded-md bg-slate-100 p-4 text-sm text-slate-600">
          Seu perfil é somente leitura. Peça a um administrador o papel de provisionador para criar recursos.
        </p>
      )}
      <div>
        <h2 className="mb-3 text-lg font-semibold">Solicitações</h2>
        <RequestList />
      </div>
    </div>
  );
}
