import type { ReactNode } from 'react';

import { AuthContext } from '@core/auth-context';

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  return (
    <AuthContext.Provider
      value={{
        userId: 'dev-user',
        email: 'dev-user@local',
        roles: ['runops.provisioner'],
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
