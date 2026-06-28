import { createFileRoute, Outlet } from '@tanstack/react-router';

import { MainLayout } from '@layouts/main-layout';

export const Route = createFileRoute('/_main')({
  component: MainShell,
});

function MainShell() {
  return (
    <MainLayout>
      <Outlet />
    </MainLayout>
  );
}
