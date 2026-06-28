import type { InputHTMLAttributes } from 'react';

import { cx } from '@ui/variants';

type InputProps = InputHTMLAttributes<HTMLInputElement>;

export function Input({ className, ...props }: InputProps) {
  return (
    <input
      data-slot="input"
      className={cx(
        'flex h-10 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200',
        className,
      )}
      {...props}
    />
  );
}
