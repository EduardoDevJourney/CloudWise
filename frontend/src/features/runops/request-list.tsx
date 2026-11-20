import { useRunopsRequests } from '@features/runops/hooks';
import { StatusBadge } from '@ui/badge';
import { Loading } from '@ui/loading';

const OUTPUT_LABELS: Record<string, string> = {
  resource_group_name: 'Resource Group',
  storage_account_name: 'Storage Account',
  key_vault_name: 'Key Vault',
};

function CreatedResources({ outputs }: { outputs: Record<string, string> }) {
  const entries = Object.entries(outputs ?? {});
  if (entries.length === 0) return <span className="text-slate-400">—</span>;

  return (
    <dl className="space-y-0.5 text-xs">
      {entries.map(([key, value]) => (
        <div key={key} className="flex gap-1">
          <dt className="text-slate-500">{OUTPUT_LABELS[key] ?? key}:</dt>
          <dd className="font-mono text-slate-800">{value}</dd>
        </div>
      ))}
    </dl>
  );
}

export function RequestList() {
  const { data, isLoading, isError, error } = useRunopsRequests();

  if (isLoading) return <Loading label="Carregando solicitações..." />;
  if (isError) return <p className="text-sm text-red-600">{(error as Error).message}</p>;
  if (!data?.length) return <p className="text-sm text-slate-500">Nenhuma solicitação ainda.</p>;

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-slate-50 text-slate-600">
          <tr>
            <th className="px-4 py-3">ID</th>
            <th className="px-4 py-3">Template</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Recursos criados</th>
            <th className="px-4 py-3">Criado em</th>
            <th className="px-4 py-3">Duração</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.id} className="border-t border-slate-100">
              <td className="px-4 py-3 font-mono text-xs">{item.id.slice(0, 8)}...</td>
              <td className="px-4 py-3">{item.template_id}</td>
              <td className="px-4 py-3">
                <StatusBadge status={item.status} />
                {item.status === 'failed' && item.error_message ? (
                  <p role="alert" className="mt-1 max-w-xs text-xs text-red-700">
                    {item.error_message}
                  </p>
                ) : null}
              </td>
              <td className="px-4 py-3">
                <CreatedResources outputs={item.outputs} />
              </td>
              <td className="px-4 py-3">{new Date(item.created_at).toLocaleString('pt-BR')}</td>
              <td className="px-4 py-3">
                {item.execution_seconds === null ? '—' : `${item.execution_seconds}s`}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
