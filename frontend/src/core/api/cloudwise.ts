import { defineApiRoute, httpResource } from '@core/http-resource';
import type { CloudWiseDashboardResponse, CostFilters, CostRecordItem } from '@core/types/api';

const COSTS_ROUTE = defineApiRoute('/api/v1/cloudwise/costs');
const DASHBOARD_ROUTE = defineApiRoute('/api/v1/cloudwise/dashboard');

function withFilters(route: string, filters: CostFilters = {}) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  const query = params.toString();
  return query ? `${route}?${query}` : route;
}

export function fetchCosts(filters?: CostFilters) {
  return httpResource<CostRecordItem[]>(withFilters(COSTS_ROUTE, filters));
}

export function fetchCloudWiseDashboard(filters?: CostFilters) {
  return httpResource<CloudWiseDashboardResponse>(withFilters(DASHBOARD_ROUTE, filters));
}
