import type { FriendlyError } from '@core/types/api';

export function describeError(error: unknown): string {
  const detail = (error as Partial<FriendlyError> | null)?.detail;
  if (Array.isArray(detail)) return detail.join(' · ');
  if (typeof detail === 'string') return detail;
  return (error as Error | null)?.message ?? 'Erro inesperado';
}
