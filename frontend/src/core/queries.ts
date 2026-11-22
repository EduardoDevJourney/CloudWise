import { queryOptions } from '@tanstack/react-query';

import { fetchMe, fetchUsers } from '@core/api/auth';
import { fetchCloudWiseDashboard, fetchCosts } from '@core/api/cloudwise';
import { fetchPolicy, fetchProvisionRequests, fetchTemplates } from '@core/api/runops';
import { queryKeys } from '@core/keys';
import type { CostFilters, ProvisionStatus } from '@core/types/api';

const TERMINAL: ProvisionStatus[] = ['success', 'failed'];

export function cloudWiseDashboardQuery(filters: CostFilters = {}) {
  return queryOptions({
    queryKey: queryKeys.cloudwise.dashboard(filters).queryKey,
    queryFn: () => fetchCloudWiseDashboard(filters),
    staleTime: 30_000,
  });
}

export function cloudWiseCostsQuery(filters: CostFilters = {}) {
  return queryOptions({
    queryKey: queryKeys.cloudwise.costs(filters).queryKey,
    queryFn: () => fetchCosts(filters),
    staleTime: 30_000,
  });
}

export const meQuery = queryOptions({
  queryKey: queryKeys.auth.me.queryKey,
  queryFn: fetchMe,
  staleTime: 60_000,
  retry: false,
});

export const usersQuery = queryOptions({
  queryKey: queryKeys.auth.users.queryKey,
  queryFn: fetchUsers,
});

export const runopsRequestsQuery = queryOptions({
  queryKey: queryKeys.runops.requests.queryKey,
  queryFn: fetchProvisionRequests,
  staleTime: 5_000,
  refetchInterval: (query) =>
    query.state.data?.some((r) => !TERMINAL.includes(r.status)) ? 3_000 : false,
});

export const runopsTemplatesQuery = queryOptions({
  queryKey: queryKeys.runops.templates.queryKey,
  queryFn: fetchTemplates,
  staleTime: 60_000,
});

export const runopsPolicyQuery = queryOptions({
  queryKey: queryKeys.runops.policy.queryKey,
  queryFn: fetchPolicy,
  staleTime: 60_000,
});
