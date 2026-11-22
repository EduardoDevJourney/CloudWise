import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import type { ProvisionStatus } from '@core/types/api';
import { StatusBadge } from '@ui/badge';

const cases: [ProvisionStatus, string, string][] = [
  ['pending', 'Pendente', 'bg-yellow-100'],
  ['running', 'Executando', 'bg-blue-100'],
  ['success', 'Sucesso', 'bg-green-100'],
  ['failed', 'Falhou', 'bg-red-100'],
];

describe('StatusBadge', () => {
  it.each(cases)('status %s has label %s and its own color', (status, label, colorClass) => {
    render(<StatusBadge status={status} />);
    const badge = screen.getByText(label);
    expect(badge).toHaveAttribute('data-variant', status);
    expect(badge).toHaveClass(colorClass);
  });
});
