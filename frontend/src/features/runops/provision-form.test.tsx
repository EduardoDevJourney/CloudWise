import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { describe, expect, it } from 'vitest';

import { renderWithClient } from '@mocks/render';
import { server } from '@mocks/server';
import { ProvisionForm } from '@features/runops/provision-form';

describe('ProvisionForm', () => {
  it('builds the template, environment and location selects from the API', async () => {
    renderWithClient(<ProvisionForm />);

    expect(await screen.findByRole('option', { name: 'Resource Group + Key Vault' })).toBeInTheDocument();
    expect(await screen.findByRole('option', { name: 'brazilsouth' })).toBeInTheDocument();
    expect(await screen.findByRole('option', { name: 'hml' })).toBeInTheDocument();
  });

  it('shows the id of the created request', async () => {
    const user = userEvent.setup();
    renderWithClient(<ProvisionForm />);
    await screen.findByRole('option', { name: 'eastus2' });

    await user.type(screen.getByRole('textbox'), 'meu-recurso');
    await user.click(screen.getByRole('button', { name: 'Provision' }));

    expect(await screen.findByText(/Request created:/)).toBeInTheDocument();
  });

  it('shows the policy violations returned with a 422', async () => {
    server.use(
      http.post('/api/v1/runops/provision', () =>
        HttpResponse.json(
          { detail: ['invalid resource_name', 'location must be one of: eastus'] },
          { status: 422 },
        ),
      ),
    );
    const user = userEvent.setup();
    renderWithClient(<ProvisionForm />);
    await screen.findByRole('option', { name: 'eastus2' });

    await user.type(screen.getByRole('textbox'), 'nome-valido');
    await user.click(screen.getByRole('button', { name: 'Provision' }));

    await waitFor(() =>
      expect(screen.getByText(/invalid resource_name · location must be one of: eastus/)).toBeInTheDocument(),
    );
  });

  it('shows the name hint and does not submit a name outside the pattern', async () => {
    let posted = false;
    server.use(
      http.post('/api/v1/runops/provision', () => {
        posted = true;
        return HttpResponse.json({}, { status: 202 });
      }),
    );
    const user = userEvent.setup();
    renderWithClient(<ProvisionForm />);
    await screen.findByRole('option', { name: 'eastus2' });

    expect(screen.getByText(/3 to 20 characters: lowercase letters, digits and hyphens/)).toBeInTheDocument();

    await user.type(screen.getByRole('textbox'), 'AB');
    expect(screen.getByRole('textbox')).toHaveAttribute('aria-invalid', 'true');
    await user.click(screen.getByRole('button', { name: 'Provision' }));

    expect(posted).toBe(false);
  });
});
