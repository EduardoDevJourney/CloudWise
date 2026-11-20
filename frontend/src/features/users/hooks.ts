import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { updateUser } from '@core/api/auth';
import { usersQuery } from '@core/queries';
import type { UserUpdate } from '@core/types/api';

export function useUsers() {
  return useQuery(usersQuery);
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, ...payload }: UserUpdate & { id: string }) => updateUser(id, payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: usersQuery.queryKey });
    },
  });
}
