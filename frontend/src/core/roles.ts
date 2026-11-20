import type { UserRole } from '@core/types/api';

export const ROLE_VIEWER: UserRole = 'runops.viewer';
export const ROLE_PROVISIONER: UserRole = 'runops.provisioner';
export const ROLE_ADMIN: UserRole = 'runops.admin';

export const ALL_ROLES: UserRole[] = [ROLE_VIEWER, ROLE_PROVISIONER, ROLE_ADMIN];

export const ROLE_LABELS: Record<UserRole, string> = {
  'runops.viewer': 'Visualizador',
  'runops.provisioner': 'Provisionador',
  'runops.admin': 'Administrador',
};

export function canProvision(role: UserRole) {
  return role === ROLE_PROVISIONER || role === ROLE_ADMIN;
}

export function isAdmin(role: UserRole) {
  return role === ROLE_ADMIN;
}
