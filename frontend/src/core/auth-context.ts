import { createContext, useContext } from 'react';

export type AuthSession = {
  userId: string;
  email: string;
  roles: string[];
};

export const AuthContext = createContext<AuthSession>({
  userId: 'dev-user',
  email: 'dev-user@local',
  roles: ['runops.provisioner'],
});

export function useAuth() {
  return useContext(AuthContext);
}
