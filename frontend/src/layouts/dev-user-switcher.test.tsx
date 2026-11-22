import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { getDevUser } from '@core/dev-users';
import { DevUserSwitcher } from '@layouts/dev-user-switcher';

describe('DevUserSwitcher', () => {
  const reload = vi.fn();

  beforeEach(() => {
    localStorage.clear();
    reload.mockClear();
    Object.defineProperty(window, 'location', { value: { reload }, writable: true });
  });

  it('lists the three profiles with the admin selected', () => {
    render(<DevUserSwitcher />);

    expect(screen.getAllByRole('option')).toHaveLength(3);
    expect(screen.getByRole('combobox', { name: 'Usuário de teste' })).toHaveValue('dev-user');
  });

  it('stores the chosen profile and reloads the page', async () => {
    render(<DevUserSwitcher />);

    await userEvent.selectOptions(screen.getByRole('combobox'), 'dev-viewer');

    expect(getDevUser().id).toBe('dev-viewer');
    expect(reload).toHaveBeenCalledOnce();
  });
});
