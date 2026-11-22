import { useQuery } from '@tanstack/react-query';

import { useAuth } from '@core/auth-context';
import { describeError } from '@core/errors';
import { usersQuery } from '@core/queries';
import { ALL_ROLES, ROLE_LABELS } from '@core/roles';
import type { UserRole } from '@core/types/api';
import { Button } from '@ui/button';
import { Loading } from '@ui/loading';
import { Select } from '@ui/select';
import { useUpdateUser } from '@features/users/hooks';

export function UserTable() {
  const { userId } = useAuth();
  const { data, isLoading, isError, error } = useQuery(usersQuery);
  const update = useUpdateUser();

  if (isLoading) return <Loading label="Carregando usuários..." />;
  if (isError) return <p className="text-sm text-red-600">{describeError(error)}</p>;
  if (!data?.length) return <p className="text-sm text-slate-500">Nenhum usuário cadastrado.</p>;

  return (
    <div className="space-y-3">
      <div className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr>
              <th className="px-4 py-3">E-mail</th>
              <th className="px-4 py-3">Papel</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Ação</th>
            </tr>
          </thead>
          <tbody>
            {data.map((user) => {
              const isSelf = user.id === userId;
              return (
                <tr key={user.id} className="border-t border-slate-100">
                  <td className="px-4 py-3">{user.email}</td>
                  <td className="px-4 py-3">
                    <Select
                      aria-label={`Papel de ${user.email}`}
                      value={user.role}
                      disabled={isSelf || update.isPending}
                      onChange={(e) => update.mutate({ id: user.id, role: e.target.value as UserRole })}
                    >
                      {ALL_ROLES.map((role) => (
                        <option key={role} value={role}>
                          {ROLE_LABELS[role]}
                        </option>
                      ))}
                    </Select>
                  </td>
                  <td className="px-4 py-3">{user.active ? 'Ativo' : 'Bloqueado'}</td>
                  <td className="px-4 py-3">
                    <Button
                      variant="secondary"
                      size="sm"
                      disabled={isSelf || update.isPending}
                      onClick={() => update.mutate({ id: user.id, active: !user.active })}
                    >
                      {user.active ? 'Bloquear' : 'Desbloquear'}
                    </Button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {update.isError ? (
        <p className="text-sm text-red-600">{describeError(update.error)}</p>
      ) : null}
    </div>
  );
}
