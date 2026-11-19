import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { createProvisionRequest } from '@core/api/runops';
import {
  runopsPolicyQuery,
  runopsRequestsQuery,
  runopsStatusQuery,
  runopsTemplatesQuery,
} from '@core/queries';
import type { ProvisionFormValues } from '@features/runops/schemas';

export function useRunopsRequests() {
  return useQuery(runopsRequestsQuery);
}

export function useTemplates() {
  return useQuery(runopsTemplatesQuery);
}

export function usePolicy() {
  return useQuery(runopsPolicyQuery);
}

export function useProvisionStatus(id: string) {
  return useQuery(runopsStatusQuery(id));
}

export function useCreateProvision() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (values: ProvisionFormValues) => createProvisionRequest(values),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: runopsRequestsQuery.queryKey });
    },
  });
}
