import { createRootRouteWithContext, Outlet } from '@tanstack/react-router';

import { AuthProvider } from '@core/auth-provider';
import type { RouterContext } from '../query-client';

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
});

function RootComponent() {
  return (
    <AuthProvider>
      <Outlet />
    </AuthProvider>
  );
}
