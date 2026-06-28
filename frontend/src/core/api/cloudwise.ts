import { defineApiRoute, httpResource } from '@core/http-resource';
import type { CloudWiseDashboardResponse, CostRecordItem } from '@core/types/api';

const COSTS_ROUTE = defineApiRoute('/api/v1/cloudwise/costs');
const DASHBOARD_ROUTE = defineApiRoute('/api/v1/cloudwise/dashboard');

export function fetchCosts() {
  return httpResource<CostRecordItem[]>(COSTS_ROUTE);
}

export function fetchCloudWiseDashboard() {
  return httpResource<CloudWiseDashboardResponse>(DASHBOARD_ROUTE);
}
