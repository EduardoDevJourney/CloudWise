import { http, HttpResponse } from 'msw';

import type { CloudWiseDashboardResponse, ProvisionRequestRead } from '@core/types/api';

const mockRequests: ProvisionRequestRead[] = [];

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
  http.get('/api/v1/cloudwise/dashboard', () => HttpResponse.json(mockDashboard)),
  http.get('/api/v1/cloudwise/costs', () => HttpResponse.json([])),
  http.get('/api/v1/runops/templates', () =>
    HttpResponse.json([
      { id: '1', slug: 'rg-storage', name: 'Resource Group + Storage Account', params_schema: {}, azure_sku: 'Standard_LRS' },
      { id: '2', slug: 'rg-keyvault', name: 'Resource Group + Key Vault', params_schema: {}, azure_sku: 'standard' },
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
  http.get('/api/v1/runops/status/:id', ({ params }) => {
    const item = mockRequests.find((r) => r.id === params.id);
    if (!item) return new HttpResponse(null, { status: 404 });
    return HttpResponse.json(item);
  }),
  http.post('/api/v1/runops/provision', async ({ request }) => {
    const body = (await request.json()) as {
      template_id: string;
      resource_name: string;
      environment: string;
      location: string;
    };
    const created: ProvisionRequestRead = {
      id: crypto.randomUUID(),
      user_id: 'dev-user',
      template_id: body.template_id,
      status: 'pending',
      request_data: body,
      error_message: null,
      created_at: new Date().toISOString(),
      execution_time: null,
    };
    mockRequests.unshift(created);
    return HttpResponse.json(created, { status: 202 });
  }),
];
