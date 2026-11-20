import { screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';

import { AuthContext } from '@core/auth-context';
import { renderWithClient } from '@mocks/render';
import { UserTable } from '@features/users/user-table';

function renderAsAdmin() {
  return renderWithClient(
    <AuthContext.Provider value={{ userId: 'dev-user', email: 'dev-user@dev.local', role: 'runops.admin' }}>
      <UserTable />
    </AuthContext.Provider>,
  );
}

describe('UserTable', () => {
  it('lista usuários e impede o admin de alterar a si mesmo', async () => {
    renderAsAdmin();
    const selfRow = (await screen.findByText('dev-user@dev.local')).closest('tr')!;
    expect(within(selfRow).getByRole('combobox')).toBeDisabled();
    expect(within(selfRow).getByRole('button', { name: 'Bloquear' })).toBeDisabled();
  });

  it('troca o papel de outro usuário', async () => {
    const user = userEvent.setup();
    renderAsAdmin();
    const select = await screen.findByLabelText('Papel de ana@corp.com');

    await user.selectOptions(select, 'runops.provisioner');

    await waitFor(() => expect(screen.getByLabelText('Papel de ana@corp.com')).toHaveValue('runops.provisioner'));
  });

  it('bloqueia e desbloqueia um usuário', async () => {
    const user = userEvent.setup();
    renderAsAdmin();
    const row = (await screen.findByText('ana@corp.com')).closest('tr')!;

    await user.click(within(row).getByRole('button', { name: 'Bloquear' }));
    expect(await within(row).findByRole('button', { name: 'Desbloquear' })).toBeInTheDocument();
    expect(within(row).getByText('Bloqueado')).toBeInTheDocument();
  });
});
