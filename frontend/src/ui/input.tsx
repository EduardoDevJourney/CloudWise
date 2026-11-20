import type { InputHTMLAttributes } from 'react';

import { cx, fieldStyles } from '@ui/variants';

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return <input className={cx(fieldStyles, className)} {...props} />;
}
