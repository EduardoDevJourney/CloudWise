import { http, HttpResponse } from 'msw';

import { DEV_USERS } from '@core/dev-users';
import type {
  CloudWiseDashboardResponse,
  ProvisionRequestCreate,
  ProvisionRequestRead,
  UserItem,
  UserUpdate,
} from '@core/types/api';

const mockRequests: ProvisionRequestRead[] = [];

const mockUsers: UserItem[] = [
  { id: 'dev-user', email: 'dev-user@dev.local', role: 'runops.admin', active: true, created_at: '2026-06-01T10:00:00Z' },
  { id: 'ana', email: 'ana@corp.com', role: 'runops.viewer', active: true, created_at: '2026-06-02T10:00:00Z' },
];

const mockDashboard: CloudWiseDashboardResponse = {
  granularity: 'day',
  series: [
    { date: '2026-06-01', total_cost: 125.5, by_service: { 'Microsoft.Storage': 125.5 } },
    { date: '2026-06-02', total_cost: 89.3, by_service: { 'Microsoft.Compute': 89.3 } },
  ],
  summary: {
    total_cost: 214.8,
    top_service: 'Microsoft.Storage',
    subscription_count: 2,
  },
};

export const handlers = [
  http.get('/api/v1/me', ({ request }) => {
    const id = request.headers.get('X-Dev-User-Id');
    const user = DEV_USERS.find((u) => u.id === id) ?? DEV_USERS[2];
    return HttpResponse.json(user);
  }),
  http.get('/api/v1/users', () => HttpResponse.json(mockUsers)),
  http.patch('/api/v1/users/:id', async ({ params, request }) => {
    const user = mockUsers.find((u) => u.id === params.id);
    if (!user) return new HttpResponse(null, { status: 404 });
    Object.assign(user, (await request.json()) as UserUpdate);
    return HttpResponse.json(user);
  }),
  http.get('/api/v1/cloudwise/dashboard', () => HttpResponse.json(mockDashboard)),
  http.get('/api/v1/cloudwise/costs', () => HttpResponse.json([])),
  http.get('/api/v1/runops/templates', () =>
    HttpResponse.json([
      { id: '1', slug: 'rg-storage', name: 'Resource Group + Storage Account', description: 'RG com Storage', params_schema: {}, azure_sku: 'Standard_LRS' },
      { id: '2', slug: 'rg-keyvault', name: 'Resource Group + Key Vault', description: 'RG com Key Vault', params_schema: {}, azure_sku: 'standard' },
    ]),
  ),
  http.get('/api/v1/runops/policy', () =>
    HttpResponse.json({
      locations: ['eastus', 'eastus2', 'brazilsouth'],
      environments: ['dev', 'hml', 'prod'],
      resource_name_pattern: '^[a-z][a-z0-9-]{2,19}$',
    }),
  ),
  http.get('/api/v1/runops/requests', () => HttpResponse.json(mockRequests)),
  http.post('/api/v1/runops/provision', async ({ request }) => {
    const body = (await request.json()) as ProvisionRequestCreate;
    const created: ProvisionRequestRead = {
      id: crypto.randomUUID(),
      user_id: 'dev-user',
      template_id: body.template_id,
      status: 'pending',
      request_data: body,
      error_message: null,
      created_at: new Date().toISOString(),
      started_at: null,
      finished_at: null,
      execution_seconds: null,
      outputs: {},
    };
    mockRequests.unshift(created);
    return HttpResponse.json(created, { status: 202 });
  }),
];
