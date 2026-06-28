import { cx } from '@ui/variants';

type LoadingProps = {
  label?: string;
};

export function Loading({ label = 'Carregando...' }: LoadingProps) {
  return (
    <div className={cx('flex items-center gap-2 text-sm text-slate-600')} data-slot="loading">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-blue-600" />
      {label}
    </div>
  );
}
