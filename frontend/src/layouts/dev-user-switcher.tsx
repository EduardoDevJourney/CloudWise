import { DEV_USERS, getDevUser, setDevUser } from '@core/dev-users';
import { ROLE_LABELS } from '@core/roles';
import { Select } from '@ui/select';

export function DevUserSwitcher() {
  return (
    <Select
      aria-label="Usuário de teste"
      className="h-8 w-auto py-0 text-xs"
      value={getDevUser().id}
      onChange={(e) => {
        setDevUser(e.target.value);
        window.location.reload();
      }}
    >
      {DEV_USERS.map((u) => (
        <option key={u.id} value={u.id}>
          {ROLE_LABELS[u.role]} ({u.email})
        </option>
      ))}
    </Select>
  );
}
