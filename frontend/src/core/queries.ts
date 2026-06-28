import { queryOptions } from '@tanstack/react-query';

import { fetchCloudWiseDashboard, fetchCosts } from '@core/api/cloudwise';
import { fetchProvisionRequests, fetchProvisionStatus } from '@core/api/runops';
import { queryKeys } from '@core/keys';
import type { ProvisionStatus } from '@core/types/api';

const TERMINAL: ProvisionStatus[] = ['success', 'failed'];

export const cloudWiseDashboardQuery = queryOptions({
  queryKey: queryKeys.cloudwise.dashboard.queryKey,
  queryFn: fetchCloudWiseDashboard,
  staleTime: 30_000,
});

export const cloudWiseCostsQuery = queryOptions({
  queryKey: queryKeys.cloudwise.costs.queryKey,
  queryFn: fetchCosts,
  staleTime: 30_000,
});

export const runopsRequestsQuery = queryOptions({
  queryKey: queryKeys.runops.requests.queryKey,
  queryFn: fetchProvisionRequests,
  staleTime: 5_000,
});

export function runopsStatusQuery(id: string) {
  return queryOptions({
    queryKey: queryKeys.runops.status(id).queryKey,
    queryFn: () => fetchProvisionStatus(id),
    enabled: Boolean(id),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (!status) return 3000;
      return TERMINAL.includes(status) ? false : 3000;
    },
  });
}
