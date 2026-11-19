import { defineApiRoute, defineApiRouteFn, httpResource } from '@core/http-resource';
import type {
  PolicyItem,
  ProvisionRequestCreate,
  ProvisionRequestRead,
  TemplateItem,
} from '@core/types/api';

const PROVISION_ROUTE = defineApiRoute('/api/v1/runops/provision');
const REQUESTS_ROUTE = defineApiRoute('/api/v1/runops/requests');
const TEMPLATES_ROUTE = defineApiRoute('/api/v1/runops/templates');
const POLICY_ROUTE = defineApiRoute('/api/v1/runops/policy');
const statusRoute = defineApiRouteFn('/api/v1/runops/status/:id');

export function fetchProvisionRequests() {
  return httpResource<ProvisionRequestRead[]>(REQUESTS_ROUTE);
}

export function fetchTemplates() {
  return httpResource<TemplateItem[]>(TEMPLATES_ROUTE);
}

export function fetchPolicy() {
  return httpResource<PolicyItem>(POLICY_ROUTE);
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
