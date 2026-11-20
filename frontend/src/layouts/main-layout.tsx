import { Link } from '@tanstack/react-router';
import type { ReactNode } from 'react';

import { useAuth } from '@core/auth-context';
import { isAdmin, ROLE_LABELS } from '@core/roles';

export function MainLayout({ children }: { children: ReactNode }) {
  const { email, role } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-lg font-semibold text-slate-900">Cloud Wise</p>
            <p className="text-sm text-slate-500">Standardized infrastructure portal</p>
          </div>
          <nav className="flex items-center gap-4 text-sm font-medium">
            <Link to="/dashboard" className="text-slate-700 hover:text-blue-600">
              Dashboard
            </Link>
            <Link to="/runops" className="text-slate-700 hover:text-blue-600">
              RunOps
            </Link>
            {isAdmin(role) ? (
              <Link to="/users" className="text-slate-700 hover:text-blue-600">
                Users
              </Link>
            ) : null}
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
              {email} · {ROLE_LABELS[role]}
            </span>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
    </div>
  );
}
