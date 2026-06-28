import type { ReactNode } from 'react';
import { Link } from '@tanstack/react-router';

type MainLayoutProps = {
  children: ReactNode;
};

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-lg font-semibold text-slate-900">Cloud Wise</p>
            <p className="text-sm text-slate-500">Cloud Proxy MVP</p>
          </div>
          <nav className="flex gap-4 text-sm font-medium">
            <Link to="/dashboard" className="text-slate-700 hover:text-blue-600">
              Dashboard
            </Link>
            <Link to="/runops" className="text-slate-700 hover:text-blue-600">
              RunOps
            </Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
    </div>
  );
}
