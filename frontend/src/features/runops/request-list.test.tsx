import { screen } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';

import { renderWithClient } from '@mocks/render';
import { server } from '@mocks/server';
import { RequestList } from '@features/runops/request-list';

const base = {
  user_id: 'dev-user',
  template_id: 'rg-storage',
  request_data: { template_id: 'rg-storage', resource_name: 'x', environment: 'dev', location: 'eastus' },
  error_message: null,
  outputs: {},
  created_at: '2026-06-01T10:00:00Z',
};

describe('RequestList', () => {
  it('mostra estado vazio', async () => {
    server.use(http.get('/api/v1/runops/requests', () => HttpResponse.json([])));
    renderWithClient(<RequestList />);
    expect(await screen.findByText('Nenhuma solicitação ainda.')).toBeInTheDocument();
  });

  it('mostra status e duração da execução', async () => {
    server.use(
      http.get('/api/v1/runops/requests', () =>
        HttpResponse.json([
          {
            ...base,
            id: 'aaaaaaaa-1',
            status: 'success',
            started_at: 'a',
            finished_at: 'b',
            execution_seconds: 42.5,
            outputs: { resource_group_name: 'rg-demo-dev', storage_account_name: 'sademodev1234' },
          },
          { ...base, id: 'bbbbbbbb-2', status: 'running', started_at: 'a', finished_at: null, execution_seconds: null },
        ]),
      ),
    );
    renderWithClient(<RequestList />);

    expect(await screen.findByText('success')).toBeInTheDocument();
    expect(screen.getByText('42.5s')).toBeInTheDocument();
    expect(screen.getByText('running')).toBeInTheDocument();
    expect(screen.getAllByText('—').length).toBeGreaterThan(0);
  });

  it('mostra os recursos criados no sucesso', async () => {
    server.use(
      http.get('/api/v1/runops/requests', () =>
        HttpResponse.json([
          {
            ...base,
            id: 'cccccccc-3',
            status: 'success',
            started_at: 'a',
            finished_at: 'b',
            execution_seconds: 10,
            outputs: { resource_group_name: 'rg-demo-dev', key_vault_name: 'kv-demo-dev-ab12' },
          },
        ]),
      ),
    );
    renderWithClient(<RequestList />);

    expect(await screen.findByText('rg-demo-dev')).toBeInTheDocument();
    expect(screen.getByText('Resource Group:')).toBeInTheDocument();
    expect(screen.getByText('kv-demo-dev-ab12')).toBeInTheDocument();
    expect(screen.getByText('Key Vault:')).toBeInTheDocument();
  });

  it('mostra a mensagem de erro quando falha', async () => {
    server.use(
      http.get('/api/v1/runops/requests', () =>
        HttpResponse.json([
          {
            ...base,
            id: 'dddddddd-4',
            status: 'failed',
            error_message: 'error: nome da Storage Account já existe',
            started_at: 'a',
            finished_at: 'b',
            execution_seconds: 3,
          },
        ]),
      ),
    );
    renderWithClient(<RequestList />);

    expect(await screen.findByRole('alert')).toHaveTextContent('nome da Storage Account já existe');
  });
});
