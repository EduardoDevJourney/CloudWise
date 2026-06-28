import { cva } from 'class-variance-authority';

import { cx } from '@ui/variants';
import type { ProvisionStatus } from '@core/types/api';

const badgeVariants = cva('inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium', {
  variants: {
    status: {
      pending: 'bg-yellow-100 text-yellow-800',
      running: 'bg-blue-100 text-blue-800',
      success: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    },
  },
  defaultVariants: {
    status: 'pending',
  },
});

type StatusBadgeProps = {
  status: ProvisionStatus;
};

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span data-slot="badge" data-variant={status} className={cx(badgeVariants({ status }))}>
      {status}
    </span>
  );
}
