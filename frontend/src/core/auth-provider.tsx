import { useQuery } from '@tanstack/react-query';
import type { ReactNode } from 'react';

import { AuthContext } from '@core/auth-context';
import { meQuery } from '@core/queries';
import type { FriendlyError } from '@core/types/api';
import { Loading } from '@ui/loading';

type AuthProviderProps = {
  children: ReactNode;
};

function AccessMessage({ title, text }: { title: string; text: string }) {
  return (
    <div className="mx-auto mt-24 max-w-md rounded-lg border border-slate-200 bg-white p-6 text-center shadow-sm">
      <h1 className="text-lg font-semibold text-slate-900">{title}</h1>
      <p className="mt-2 text-sm text-slate-600">{text}</p>
    </div>
  );
}

export function AuthProvider({ children }: AuthProviderProps) {
  const { data, isLoading, error } = useQuery(meQuery);

  if (isLoading) return <Loading label="Verificando acesso..." />;

  if (error || !data) {
    const status = (error as FriendlyError | null)?.status;
    if (status === 403) {
      return (
        <AccessMessage
          title="Acesso bloqueado"
          text="Sua conta foi bloqueada. Procure um administrador do Cloud Wise."
        />
      );
    }
    if (status === 401) {
      return (
        <AccessMessage
          title="Não autenticado"
          text="Entre com sua conta corporativa para acessar o Cloud Wise."
        />
      );
    }
    return (
      <AccessMessage title="Erro ao carregar" text="Não foi possível verificar seu acesso. Tente novamente." />
    );
  }

  return (
    <AuthContext.Provider value={{ userId: data.id, email: data.email, role: data.role }}>
      {children}
    </AuthContext.Provider>
  );
}
