import { useMutation, useQueryClient } from '@tanstack/react-query';

import { createProvisionRequest } from '@core/api/runops';
import { runopsRequestsQuery } from '@core/queries';

export function useCreateProvision() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createProvisionRequest,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: runopsRequestsQuery.queryKey });
    },
  });
}
