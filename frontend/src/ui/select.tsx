import type { SelectHTMLAttributes } from 'react';

import { cx, fieldStyles } from '@ui/variants';

export function Select({ className, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
  return <select className={cx(fieldStyles, className)} {...props} />;
}
