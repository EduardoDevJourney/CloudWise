import { useQuery } from '@tanstack/react-query';
import type { ReactNode } from 'react';

import { AuthContext } from '@core/auth-context';
import { meQuery } from '@core/queries';
import type { FriendlyError } from '@core/types/api';
import { Loading } from '@ui/loading';

function AccessMessage({ title, text }: { title: string; text: string }) {
  return (
    <div className="mx-auto mt-24 max-w-md rounded-lg border border-slate-200 bg-white p-6 text-center shadow-sm">
      <h1 className="text-lg font-semibold text-slate-900">{title}</h1>
      <p className="mt-2 text-sm text-slate-600">{text}</p>
    </div>
  );
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data, isLoading, error } = useQuery(meQuery);

  if (isLoading) return <Loading label="Checking access..." />;

  if (error || !data) {
    const status = (error as FriendlyError | null)?.status;
    if (status === 403) {
      return (
        <AccessMessage
          title="Access blocked"
          text="Your account has been blocked. Contact a Cloud Wise admin."
        />
      );
    }
    if (status === 401) {
      return (
        <AccessMessage
          title="Not authenticated"
          text="Sign in with your company account to use Cloud Wise."
        />
      );
    }
    return (
      <AccessMessage title="Failed to load" text="We couldn't verify your access. Try again." />
    );
  }

  return (
    <AuthContext.Provider value={{ userId: data.id, email: data.email, role: data.role }}>
      {children}
    </AuthContext.Provider>
  );
}
