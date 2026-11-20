import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';

import { renderWithClient } from '@mocks/render';
import { server } from '@mocks/server';
import { ProvisionForm } from '@features/runops/provision-form';

describe('ProvisionForm', () => {
  it('monta os selects de template, ambiente e região a partir da API', async () => {
    renderWithClient(<ProvisionForm />);

    expect(await screen.findByRole('option', { name: 'Resource Group + Key Vault' })).toBeInTheDocument();
    expect(await screen.findByRole('option', { name: 'brazilsouth' })).toBeInTheDocument();
    expect(await screen.findByRole('option', { name: 'hml' })).toBeInTheDocument();
  });

  it('mostra o id da solicitação criada', async () => {
    const user = userEvent.setup();
    renderWithClient(<ProvisionForm />);
    await screen.findByRole('option', { name: 'eastus2' });

    await user.type(screen.getByRole('textbox'), 'meu-recurso');
    await user.click(screen.getByRole('button', { name: 'Provisionar' }));

    expect(await screen.findByText(/Solicitação criada:/)).toBeInTheDocument();
  });

  it('mostra as violações de política devolvidas com 422', async () => {
    server.use(
      http.post('/api/v1/runops/provision', () =>
        HttpResponse.json(
          { detail: ['resource_name inválido', 'location deve ser uma de: eastus'] },
          { status: 422 },
        ),
      ),
    );
    const user = userEvent.setup();
    renderWithClient(<ProvisionForm />);
    await screen.findByRole('option', { name: 'eastus2' });

    await user.type(screen.getByRole('textbox'), 'ab');
    await user.click(screen.getByRole('button', { name: 'Provisionar' }));

    await waitFor(() =>
      expect(screen.getByText(/resource_name inválido · location deve ser uma de: eastus/)).toBeInTheDocument(),
    );
  });
});
