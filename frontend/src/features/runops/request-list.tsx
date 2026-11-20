import { useRunopsRequests } from '@features/runops/hooks';
import { StatusBadge } from '@ui/badge';
import { Loading } from '@ui/loading';

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
