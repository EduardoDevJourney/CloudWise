import { createQueryKeyStore } from '@lukemorales/query-key-factory';

export const queryKeys = createQueryKeyStore({
  cloudwise: {
    costs: null,
    dashboard: null,
  },
  runops: {
    requests: null,
    templates: null,
    policy: null,
    status: (id: string) => [id],
  },
});
