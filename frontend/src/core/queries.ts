import { queryOptions } from '@tanstack/react-query';

import { fetchCloudWiseDashboard, fetchCosts } from '@core/api/cloudwise';
import {
  fetchPolicy,
  fetchProvisionRequests,
  fetchProvisionStatus,
  fetchTemplates,
} from '@core/api/runops';
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
  // Enquanto houver solicitação em andamento, atualiza a lista sozinha.
  refetchInterval: (query) =>
    query.state.data?.some((r) => !TERMINAL.includes(r.status)) ? 3000 : false,
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
