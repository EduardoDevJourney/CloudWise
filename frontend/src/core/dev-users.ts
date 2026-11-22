import { ROLE_ADMIN, ROLE_PROVISIONER, ROLE_VIEWER } from '@core/roles';
import type { UserRole } from '@core/types/api';

export type DevUser = { id: string; email: string; role: UserRole };

export const DEV_USERS: DevUser[] = [
  { id: 'dev-viewer', email: 'viewer@dev.local', role: ROLE_VIEWER },
  { id: 'dev-provisioner', email: 'provisioner@dev.local', role: ROLE_PROVISIONER },
  { id: 'dev-user', email: 'dev-user@dev.local', role: ROLE_ADMIN },
];

const STORAGE_KEY = 'cloud-wise-dev-user';
const DEFAULT_USER = DEV_USERS[2];

export function getDevUser(): DevUser {
  try {
    const id = localStorage.getItem(STORAGE_KEY);
    return DEV_USERS.find((u) => u.id === id) ?? DEFAULT_USER;
  } catch {
    return DEFAULT_USER;
  }
}

export function setDevUser(id: string) {
  try {
    localStorage.setItem(STORAGE_KEY, id);
  } catch {
    // no storage available: keeps the default user
  }
}
