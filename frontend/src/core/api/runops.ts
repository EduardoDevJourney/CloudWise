import { defineApiRoute, defineApiRouteFn, httpResource } from '@core/http-resource';
import type { ProvisionRequestCreate, ProvisionRequestRead } from '@core/types/api';

const PROVISION_ROUTE = defineApiRoute('/api/v1/runops/provision');
const REQUESTS_ROUTE = defineApiRoute('/api/v1/runops/requests');
const statusRoute = defineApiRouteFn('/api/v1/runops/status/:id');

export function fetchProvisionRequests() {
  return httpResource<ProvisionRequestRead[]>(REQUESTS_ROUTE);
}

export function fetchProvisionStatus(id: string) {
  return httpResource<ProvisionRequestRead>(statusRoute(id));
}

export function createProvisionRequest(payload: ProvisionRequestCreate) {
  return httpResource<ProvisionRequestRead>(PROVISION_ROUTE, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
