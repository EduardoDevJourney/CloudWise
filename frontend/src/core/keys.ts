import { createQueryKeyStore } from '@lukemorales/query-key-factory';

export const queryKeys = createQueryKeyStore({
  cloudwise: {
    costs: (filters: object) => [filters],
    dashboard: (filters: object) => [filters],
  },
  auth: {
    me: null,
    users: null,
  },
  runops: {
    requests: null,
    templates: null,
    policy: null,
    status: (id: string) => [id],
  },
});
