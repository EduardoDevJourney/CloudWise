import { cva } from 'class-variance-authority';

import type { ProvisionStatus } from '@core/types/api';

const badgeVariants = cva(
  'inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium',
  {
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
  },
);

const dotVariants = cva('h-1.5 w-1.5 rounded-full', {
  variants: {
    status: {
      pending: 'bg-yellow-500',
      running: 'animate-pulse bg-blue-500',
      success: 'bg-green-500',
      failed: 'bg-red-500',
    },
  },
});

const STATUS_LABELS: Record<ProvisionStatus, string> = {
  pending: 'Pending',
  running: 'Running',
  success: 'Success',
  failed: 'Failed',
};

export function StatusBadge({ status }: { status: ProvisionStatus }) {
  return (
    <span data-variant={status} className={badgeVariants({ status })}>
      <span aria-hidden="true" className={dotVariants({ status })} />
      {STATUS_LABELS[status]}
    </span>
  );
}
