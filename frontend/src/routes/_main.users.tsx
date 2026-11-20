import { createFileRoute } from '@tanstack/react-router';

import { useAuth } from '@core/auth-context';
import { isAdmin } from '@core/roles';
import { UserTable } from '@features/users/user-table';

export const Route = createFileRoute('/_main/users')({
  component: UsersPage,
});

function UsersPage() {
  const { role } = useAuth();

  if (!isAdmin(role)) {
    return <p className="text-sm text-slate-600">Only admins can manage users.</p>;
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-slate-900">Users</h1>
      <UserTable />
    </div>
  );
}
