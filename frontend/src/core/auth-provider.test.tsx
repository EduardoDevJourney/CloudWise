import { screen } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';

import { useAuth } from '@core/auth-context';
import { AuthProvider } from '@core/auth-provider';
import { renderWithClient } from '@mocks/render';
import { server } from '@mocks/server';

function Who() {
  const { email, role } = useAuth();
  return <p>{`${email} / ${role}`}</p>;
}

describe('AuthProvider', () => {
  it('expõe usuário e papel vindos de /me', async () => {
    renderWithClient(
      <AuthProvider>
        <Who />
      </AuthProvider>,
    );
    expect(await screen.findByText('dev-user@dev.local / runops.admin')).toBeInTheDocument();
  });

  it('mostra tela de não autenticado em 401', async () => {
    server.use(http.get('/api/v1/me', () => HttpResponse.json({ detail: 'Authentication required' }, { status: 401 })));
    renderWithClient(
      <AuthProvider>
        <Who />
      </AuthProvider>,
    );
    expect(await screen.findByText('Não autenticado')).toBeInTheDocument();
  });

  it('mostra tela de acesso bloqueado em 403', async () => {
    server.use(http.get('/api/v1/me', () => HttpResponse.json({ detail: 'User blocked' }, { status: 403 })));
    renderWithClient(
      <AuthProvider>
        <Who />
      </AuthProvider>,
    );
    expect(await screen.findByText('Acesso bloqueado')).toBeInTheDocument();
  });
});
