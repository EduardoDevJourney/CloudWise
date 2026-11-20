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
          { ...base, id: 'aaaaaaaa-1', status: 'success', started_at: 'a', finished_at: 'b', execution_seconds: 42.5 },
          { ...base, id: 'bbbbbbbb-2', status: 'running', started_at: 'a', finished_at: null, execution_seconds: null },
        ]),
      ),
    );
    renderWithClient(<RequestList />);

    expect(await screen.findByText('success')).toBeInTheDocument();
    expect(screen.getByText('42.5s')).toBeInTheDocument();
    expect(screen.getByText('running')).toBeInTheDocument();
    expect(screen.getByText('—')).toBeInTheDocument();
  });
});
