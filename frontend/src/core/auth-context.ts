import { createContext, useContext } from 'react';

import type { UserRole } from '@core/types/api';

type AuthSession = {
  userId: string;
  email: string;
  role: UserRole;
};

export const AuthContext = createContext<AuthSession>({
  userId: '',
  email: '',
  role: 'runops.viewer',
});

export function useAuth() {
  return useContext(AuthContext);
}
