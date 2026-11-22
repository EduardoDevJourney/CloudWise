import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';

import { renderWithClient } from '@mocks/render';
import { server } from '@mocks/server';
import { CloudWiseDashboard } from '@features/cloudwise/dashboard';

describe('CloudWiseDashboard', () => {
  it('envia os filtros escolhidos para a API', async () => {
    const seen: string[] = [];
    server.use(
      http.get('/api/v1/cloudwise/costs', () =>
        HttpResponse.json([
          { id: '1', subscription_id: 'sub-1', cost: 1, date: '2026-06-01', resource_type: 'Microsoft.Storage', tags: {} },
          { id: '2', subscription_id: 'sub-2', cost: 2, date: '2026-06-02', resource_type: 'Microsoft.Compute', tags: {} },
        ]),
      ),
      http.get('/api/v1/cloudwise/dashboard', ({ request }) => {
        seen.push(new URL(request.url).search);
        return HttpResponse.json({
          granularity: 'day',
          series: [],
          summary: { total_cost: 0, top_service: 'n/a', subscription_count: 0 },
        });
      }),
    );
    const user = userEvent.setup();
    renderWithClient(<CloudWiseDashboard />);

    await screen.findByRole('option', { name: 'Microsoft.Compute' });
    await user.selectOptions(screen.getByLabelText('Serviço'), 'Microsoft.Compute');

    await waitFor(() => expect(seen).toContain('?service=Microsoft.Compute'));
    expect(await screen.findByText('Sem dados para o filtro selecionado.')).toBeInTheDocument();
  });

  it('shows the cost per day and per service charts', async () => {
    renderWithClient(<CloudWiseDashboard />);

    expect(await screen.findByText('Custo por dia')).toBeInTheDocument();
    expect(screen.getByText('Custo por serviço')).toBeInTheDocument();
    expect(screen.getByTestId('chart-daily')).toBeInTheDocument();
    expect(screen.getByTestId('chart-services')).toBeInTheDocument();
  });
});
