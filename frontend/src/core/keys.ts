import { createQueryKeyStore } from '@lukemorales/query-key-factory';

export const queryKeys = createQueryKeyStore({
  cloudwise: {
    costs: null,
    dashboard: null,
  },
  runops: {
    requests: null,
    status: (id: string) => [id],
  },
});
