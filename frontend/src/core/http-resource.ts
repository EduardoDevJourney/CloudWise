import type { FriendlyError } from '@core/types/api';

const API_BASE = import.meta.env.VITE_API_URL ?? '';

export function defineApiRoute(path: string) {
  return `${API_BASE}${path}`;
}

export function defineApiRouteFn(path: string) {
  return (id: string) => `${API_BASE}${path.replace(':id', id)}`;
}

async function parseError(response: Response): Promise<FriendlyError> {
  try {
    const data = await response.json();
    return {
      title: data.title ?? 'Request failed',
      detail: data.detail ?? response.statusText,
      status: response.status,
    };
  } catch {
    return {
      title: 'Request failed',
      detail: response.statusText,
      status: response.status,
    };
  }
}

export async function httpResource<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  headers.set('Content-Type', 'application/json');
  headers.set('Accept', 'application/json');
  headers.set('X-Dev-User-Id', 'dev-user');
  headers.set('X-Dev-User-Email', 'dev-user@dev.local');

  const response = await fetch(input, { ...init, headers });

  if (!response.ok) {
    throw await parseError(response);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
